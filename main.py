from Service.AntenaImporterService import AntenaImporterService
# from Repository.ItemRepository import ItemRepository
from Service.ItemService import ItemService

def main():
   # item_service = ItemService()
   # item_service.fix_pppoe()
   antena_importer = AntenaImporterService()
   antena_importer.importar()
main()