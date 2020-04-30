(define (domain play_murder_domain)
    (:types  person item role element - object
    step literal - element
		)
    (:predicates
        (hate ?p1 - person ?p2 - person)
        (stageProperty ?i - item)
        (weapon ?i - item)
        (set ?i - item)
        (takeRole ?p - person ?r - role)
        (planMurder ?m - person)
        (killed ?m - person ?v - person)
        (onPlay ?m - person ?v - person)
        (moreImportant ?r1 - role ?r2 - role)
        )

    (:action argue_often
        :parameters (?m - person ?v - person)
        :precondition (hate ?m ?v)
        :effect(planMurder ?m))

    (:action stage_setting
        :parameters (?i - item)
        :precondition (and(not(set ?i))
                        (stageProperty ?i))
        :effect (set ?i))

    (:action play_open
        :parameters (?v - person ?r1 - role ?m - person ?r2 - role ?i - item)
        :precondition (and (takeRole ?v ?r1)
                        (takeRole ?m ?r2)
                        (set ?i))
        :effect (onPlay ?m ?v))

    (:action change_knife
        :parameters (?m - person ?fk - item ?rk - item)
        :precondition (and (stageProperty ?fk)
                            (weapon ?rk)
                            (set ?fk)
                            (planMurder ?m))
        :effect (and (not (set ?fk))
                        (set ?rk)))

    (:action murder_on_play
        :parameters (?m - person ?v - person ?i - item)
        :precondition (and (weapon ?i)
                        (set ?i)
                        (onPlay ?m ?v))
        :effect (killed ?m ?v))


    (:action want_to_change_role
        :parameters (?p - person ?r1 - role ?r2 - role)
        :precondition (and (takeRole ?p ?r1)
                        (moreImportant ?r2 ?r1))
        :effect (planMurder ?p))
)

