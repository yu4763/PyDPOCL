(define (problem play_murder_problem)
    (:domain play_murder_domain)

    (:objects Ann Alex Diana - person
              roleA roleB roleC - role
              FakeKnife RealKnife - item)

    (:init
        (stageProperty FakeKnife)
        (weapon RealKnife)
        (takeRole Alex roleA)
        (takeRole Ann roleB)
        (takeRole Diana roleC)
        (moreImportant roleB roleC)
        (hate Ann Alex)
    )

    (:goal
        (killed Ann Alex)
    )
)
