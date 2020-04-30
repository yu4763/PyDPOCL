(define (problem play_murder_problem)
    (:domain play_murder_domain)

    (:objects Ann Alex Diana - person
              starring supporting - role
              FakeKnife RealKnife - item)

    (:init
        (stageProperty FakeKnife)
        (weapon RealKnife)
        (takeRole Alex starring)
        (takeRole Ann starring)
        (takeRole Diana supporting)
        (moreImportant starring supporting)
        (hate Ann Alex)
    )

    (:goal
        (killed Ann Alex)
    )
)
