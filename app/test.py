from modules import ModuleEventSource
from filter import ModuleSubject
from triangulation import FilterSubject

def main():
    moduleEventSource = ModuleEventSource
    moduleSubject = ModuleSubject()
    filterSubject = FilterSubject()

    # # Need to add subscribe behaviour before events are re-emitted from the filter
    # moduleSubject.subscribe(
    #     on_next = lambda audioItem: filterSubject.on_next(audioItem),
    #     on_error = lambda e: filterSubject.on_error(e),
    #     on_completed = lambda: filterSubject.on_completed()
    # )

    # # On subscription, produce_events() is called
    moduleEventSource.subscribe(
        on_next = lambda audioItem: moduleSubject.on_next(audioItem),
        on_error = lambda e: moduleSubject.on_error(e),
        on_completed = lambda: moduleSubject.on_completed()
    )

    print("Exiting.")
    exit()

if __name__ == '__main__':
    main()
