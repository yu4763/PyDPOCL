(define (problem tower_detective_problem)
    (:domain tower_detective_domain)

    (:objects Ann Alex Diana - person
              School - location
              Car Clock - item)

    (:init
        (alarm Diana Car)
    )

    (:goal
        (and (married Alex)
        (marryWith Alex Ann)
        (single Diana)
        (workAt Alex School)
        (workAt Diana School)
        (have Alex Car)
        (tower Clock))
    )
)
