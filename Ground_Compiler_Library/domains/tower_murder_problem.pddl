(define (problem tower_murder_problem)
    (:domain tower_murder_domain)

    (:objects Ann Alex Diana - person
              School - location
              Car Clock - item)

    (:init
        (married Alex)
        (marryWith Alex Ann)
        (single Diana)
        (workAt Alex School)
        (workAt Diana School)
        (have Alex Car)
        (tower Clock)
    )

    (:goal
        (alarm Diana Car)
    )
)
