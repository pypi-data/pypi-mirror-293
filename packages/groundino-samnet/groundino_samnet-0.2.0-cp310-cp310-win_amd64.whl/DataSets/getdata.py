import os
import zipfile
from PIL import Image
import torch
import tempfile
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
import shutil
from typing import Optional, Union, Tuple
from glob import glob

class PermuteTensor():
    def __init__(self, dim):
        self.dim = dim

    def __call__(self, tensor):
        return tensor.permute(self.dim)

class ToBoolTensor(transforms.ToTensor):
    def __call__(self, pic):
        tensor = super().__call__(pic)
        tensor = tensor.float()
        return tensor > 0.5

class ToFloatTensor(transforms.ToTensor):
    def __call__(self, pic):
        tensor = super().__call__(pic)
        return tensor.float()

class Mamitas_Create_Dataset(Dataset):
    def __init__(self, 
                 file_images: list, 
                 file_masks: list,
                 merge_image: bool,
                 transform_mask: transforms.Compose,
                 transform_img: transforms.Compose,
                 dataset: str):
        
        self.file_images = file_images
        self.file_masks = file_masks
        self.transform_mask = transform_mask
        self.transform_img = transform_img
        self.merge_image = merge_image
        self.dataset = dataset

    def __len__(self) -> int:
        return len(self.file_images)

    def __getitem__(self, 
                    idx: int) -> Tuple[torch.Tensor,torch.Tensor,str]:
        root_name_img = self.file_images[idx]
        root_name_mask = self.file_masks[idx]

        img, mask, id_image = thermal_feet_dataset.load_instance(root_name_img,
                                                                         root_name_mask,
                                                                         self.merge_image,
                                                                         self.transform_mask,
                                                                         self.transform_img,
                                                                         self.dataset)

        return img, mask, id_image

class thermal_feet_dataset():
    def __init__(self,dataset:str,credentials_path:str):
        self.__path_file = os.path.abspath(__file__)
        self.dataset = dataset
        self.credentials_path = credentials_path
        self.file_imgs = []
        self.file_masks = []
        
        # Crear el directorio temporal y almacenar la referencia
        self.temp_dir = tempfile.TemporaryDirectory()
        self.final_path_zip_m = os.path.join(self.temp_dir.name, 'mamitas')
        self.final_path_m = os.path.join(self.final_path_zip_m,'data')



        self.final_path_zip_i = os.path.join(self.temp_dir.name,'infrared')
        self.final_path_i = os.path.join(self.final_path_zip_i,'data')
        self.workspace = os.path.join(self.final_path_i,'dataset')
        
        self.download_by_kaggle(self.dataset)


        if self.dataset == 'mtf':
            for carpet in os.listdir(self.final_path_m):
                for files in os.listdir(os.path.join(self.final_path_m, carpet, 'Imágenes')):
                    path_file = os.path.join(self.final_path_m, carpet, 'Imágenes', files)
                    self.file_imgs.append(path_file)
                    self.file_masks.append(os.path.join(self.final_path_m, carpet, 'Máscaras - Manuales', path_file.split(os.sep)[-1][:-4] + ".png"))
                #for files in os.listdir(os.path.join(self.final_path, carpet, 'Máscaras - Manuales')):
                    #self.file_masks.append(os.path.join(self.final_path, carpet, 'Máscaras - Manuales', files))
            assert len(self.file_imgs) == len(self.file_masks), 'El número de imágenes y sus máscaras no coinciden.'

        elif self.dataset == 'itf':
            self.file_imgs = glob(os.path.join(self.workspace, '*[!(mask)].jpg'))
            self.file_masks = [self.convert_to_mask_path(path) for path in self.file_imgs]

    def convert_to_mask_path(self,image_path: str) -> str:
        """
        Convert an image path to its corresponding mask path.

        Args:
            image_path (str): Path to the image file.

        Returns:
            str: Path to the corresponding mask file.
        """
        # Obtener el directorio y el nombre del archivo sin la extensión
        directory, file_name = os.path.split(image_path)
        file_name_no_ext, _ = os.path.splitext(file_name)
        
        # Construir el nuevo nombre del archivo con '_mask' y cambiar la extensión a .png
        mask_file_name = f"{file_name_no_ext}_mask.png"
        
        # Construir y devolver la nueva ruta
        mask_path = os.path.join(directory, mask_file_name)
        return mask_path
    
    def download_by_kaggle(self, dataset):
        try:
            credential = self.credentials_path
            if not os.path.isfile(credential):
                raise FileNotFoundError(f"No se encontró el archivo kaggle.json en {credential}")
            dest_folder = os.path.expanduser('~/.kaggle/')
            os.makedirs(dest_folder, exist_ok=True)
            shutil.copy(credential, dest_folder)

            from kaggle.api.kaggle_api_extended import KaggleApi
            api = KaggleApi()
            api.authenticate()
            
            dataset_ids = {
                "mtf": 'lucasiturriago/mamitas-thermal-feet',
                "itf": 'wilhelmbuitrago18/infrared-thermal-feet'
            }

            path_zip = {
                "mtf": self.final_path_zip_m,
                "itf": self.final_path_zip_i
            }
            path_final = {
                "mtf": self.final_path_m ,
                "itf": self.final_path_i
            }
            print("apigood")
            if dataset in dataset_ids:
                dataset_id = dataset_ids[dataset]
                api.dataset_download_files(dataset_id, path=path_zip[dataset])

                for file_name in os.listdir(path_zip[dataset]):
                    if file_name.endswith('.zip'):
                        zip_path = os.path.join(path_zip[dataset], file_name)
                        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                            zip_ref.extractall(path_final[dataset])
                        break
                    
        except FileNotFoundError as e:
            print(f"Error: {e}")
            self.cleanup()
        
        except Exception as e:
            print(f"Error al cargar las credenciales o descargar el dataset: {e}")
            self.cleanup()

    def cleanup(self):
        """Cierra y elimina el directorio temporal."""
        self.temp_dir.cleanup()

    @staticmethod
    def load_instance(root_name_img: str,
                      root_name_mask: str,
                      merge_image: bool,
                      transform_mask: transforms.Compose,
                      transform_img: transforms.Compose,
                      dataset: str) -> Tuple[torch.Tensor,torch.Tensor,str]:
        """
        Load an instance from the dataset

        Args:
          root_name_img (str): Path to image file
          root_name_mask (str): Path to mask file

        Returns:
          img (torch.Tensor): Image tensor
          mask (torch.Tensor): Mask tensor
        """

        img = Image.open(root_name_img).convert('L')
        mask = Image.open(root_name_mask).convert('L')
        if merge_image:
           img = Image.merge('RGB',(img,img,img))
        if transform_mask is not None:
          mask = thermal_feet_dataset.__preprocessing_mask(mask,transform_mask)
        if transform_img is not None:
          img = thermal_feet_dataset.__preprocessing_img(img,transform_img)
        id_image = thermal_feet_dataset.extract_id(root_name_img,dataset)
        return img, mask, id_image

    @staticmethod
    def __preprocessing_mask(mask: Image.Image,
                             transforms: transforms.Compose) -> torch.Tensor:
        """
        Transforms a PIL Image

        Args:
            img (PIL Image): PIL Image to transform
        Returns:
            PIL Image: Transformed PIL Image
        """
        #transform = transforms.Compose([
            #transforms.Resize((224, 224)),
            #ToBoolTensor(),
        #])
        mask = transforms(mask)
        return mask

    @staticmethod
    def __preprocessing_img(img: Image.Image,
                            transforms: transforms.Compose) -> torch.Tensor:
      """
      Transforms a PIL Image

      Args:
          img (PIL Image): PIL Image to transform
      Returns:
          PIL Image: Transformed PIL Image
      """
      #transform = transforms.Compose([
          #transforms.Resize((224, 224)),
          #ToFloatTensor(),
      #])
      img = transforms(img)
      return img

    @staticmethod
    def extract_id(path: str, dataset:str) -> str:
      """
      Extract de id for image file

      Args:
        path (str): Path to image file
      Returns:
        str: Id for image file
      """
      if dataset == "mtf":
        path_parts = os.path.normpath(path).split(os.sep)
        case_part = path_parts[-3]
        image_name = os.path.splitext(path_parts[-1])[0]
        result = case_part + image_name
      elif dataset == "itf":
         result = os.path.split(path)[-1][:-4]
      return result

    def __call__(self):
        return self

    def generate_dataset_with_val(self,
                                  transform_mask: transforms.Compose,
                                  transform_img: transforms.Compose,
                                  merge_image: bool = True,
                                  torch_dataset: bool = False,
                                  batch_size: Optional[int] = 32,
                                  shuffle: Optional[bool] = True,
                                  split_val: float=0.2,
                                  seed:int = 42) -> Union[Tuple[DataLoader,DataLoader],Tuple[Dataset,Dataset]]:
      """
      Generate a dataset with validation split

      Args:
        torch_dataset (bool): If True, returns a torch Dataset object (Optional).
        batch_size (int): Batch size for the dataset (Optional).
        shuffle (bool): Whether to shuffle the dataset (Optional).
        split_val (float): Validation split ratio.
        seed (int): Random seed for shuffling.

      Returns:
        Dataset or DataLoader object.
      """

      train_imgs, val_imgs, train_masks, val_masks = train_test_split(self.file_imgs,
                                                                      self.file_masks,
                                                                      test_size=split_val,
                                                                      random_state=seed)

      print(f"Train_dataset: {len(train_imgs)}")
      print(f"Val_dataset: {len(val_imgs)}")
      train_dataset = Mamitas_Create_Dataset(train_imgs,
                                             train_masks,
                                             merge_image,
                                             transform_mask,
                                             transform_img,
                                             self.dataset)

      val_dataset = Mamitas_Create_Dataset(val_imgs,
                                           val_masks,
                                           merge_image,
                                           transform_mask,
                                           transform_img,
                                           self.dataset)

      if torch_dataset:
        assert batch_size is not None and shuffle is not None, "batch_size and shuffle must be provided when torch_dataset is True"
        return DataLoader(train_dataset, batch_size=batch_size, shuffle=shuffle), DataLoader(val_dataset, batch_size=batch_size, shuffle=shuffle)

      return train_dataset, val_dataset

    def generate_dataset(self,
                         transform_mask:transforms.Compose,
                         transform_img:transforms.Compose,
                         merge_image: bool = True,
                         torch_dataset: Optional[bool]= False,
                         batch_size: Optional[int] = 32,
                         shuffle: Optional[bool] = True) -> Union[Dataset, DataLoader]:
      """
      Generate a dataset

      Args:
        torch_dataset (bool): If True, returns a torch Dataset object (Optional).
        batch_size (int): Batch size for the dataset (Optional).
        shuffle (bool): Whether to shuffle the dataset (Optional).

      Returns:
        Dataset or DataLoader object.
      """

      dataset = Mamitas_Create_Dataset(self.file_imgs,
                                       self.file_masks,
                                       merge_image,
                                       transform_mask,
                                       transform_img,
                                       self.dataset)

      if torch_dataset:
        assert batch_size is not None and shuffle is not None, "batch_size and shuffle must be provided when torch_dataset is True"
        return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)

      return dataset
    

if __name__ == "__main__":
  thermal_feet_dataset()