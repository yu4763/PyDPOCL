(define (problem play_detective_problem_a)
    (:domain play_detective_domain)

    (:objects Ann Alex Diana - person
              starring supporting - role
              FakeKnife RealKnife - item)

    (:init
        (killed Ann Alex)
    )

    (:goal
        (and (stageProperty FakeKnife)
        (weapon RealKnife)
        (takeRole Alex starring)
        (takeRole Ann starring)
        (hate Ann Alex))
    )
)
