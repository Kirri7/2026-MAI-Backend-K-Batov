from cache import LRUCache
CACHE_SIZE = 100

def main():
    cache = LRUCache(CACHE_SIZE)
    cache.set('Jesse', 'Pinkman')
    cache.set('Walter', 'White')
    cache.set('Jesse', 'James')
    print(cache.get('Jesse')) # вернёт 'James'
    cache.rem('Walter')
    print(cache.get('Walter') or 'empty') # вернёт ''
    # Волтер, почисти кэш, Волтер
    for i in range(CACHE_SIZE-1):
        cache.set(str(i), str(i) * 2)
    
    print(cache.get('Jesse') or 'empty') # вернёт 'James'
    cache.set('finish', 'him')
    print(cache.get('Jesse') or 'empty') # вернёт ''


if __name__ == "__main__": 
    # показывает, что скрипт предзназначен для исполнения, а не импорта
    main()