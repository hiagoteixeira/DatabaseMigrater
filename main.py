from Service.AntenaImporterService import AntenaImporterService
# from Repository.ItemRepository import ItemRepository


def main():
    antenaImporterService = AntenaImporterService()
    antenaImporterService.importar()
    # itemRepository = ItemRepository()
    # itemRepository.get_by_serie(200005)
    

main()