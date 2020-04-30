(define (domain tower_detective_domain)
    (:types  person location item element - object
    step literal - element
		)
    (:predicates
        (married ?p - person)
        (single ?p - person)
        (marryWith ?p1 - person ?p2 - person)
        (workAt ?p - person ?l - location)
        (have ?p - person ?i - item)
        (affair ?p1 - person ?p2 - person)
        (love ?p1 - person ?p2 - person)
        (planToKill ?m - person ?v - person)
        (killed ?m - person ?v - person)
        (existUnderTower ?i - item)
        (bodyOnTheClock ?p - person ?i - item)
        (afternoon ?i - item)
        (alarm ?p - person ?i - item)
        (tower ?i - item)
        (setUpAlibi ?p - person)
        )

    (:action have_an_affair
        :parameters (?p1 - person ?p2 - person)
        :precondition (affair ?p1 ?p2)
        :effect (and (married ?p1)
                      (single ?p2)
                      (love ?p1 ?p2)
                      (love ?p2 ?p1)))

    (:action fall_in_love
        :parameters (?p1 - person ?p2 - person ?l - location)
        :precondition (and (love ?p1 ?p2)
                    (love ?p2 ?p1))
        :effect (and (workAt ?p1 ?l)
                      (workAt ?p2 ?l)))

    (:action want_to_reveal_affair_to
        :parameters (?p1 - person ?p2 - person ?p3 - person)
        :precondition (and(planToKill ?p1 ?p2)
                    (setUpAlibi ?p1))
        :effect (and (affair ?p1 ?p2)
                      (marryWith ?p1 ?p3)))

    (:action park_under_clock_tower
        :parameters (?m - person ?car - item ?clock - item)
        :precondition (existUnderTower ?car)
        :effect (and (have ?m ?car)
                        (not(afternoon ?clock))
                        (tower ?clock)
                        (setUpAlibi ?m)))

    (:action murder
        :parameters (?m - person ?v - person)
        :precondition (killed ?m ?v)
        :effect (planToKill ?m ?v))

    (:action put_body_on_the_clock
        :parameters (?m - person ?v - person ?i - item)
        :precondition (bodyOnTheClock ?v ?i)
        :effect (and (killed ?m ?v)
                        (tower ?i)))

    (:action afternoon_body_fall
        :parameters (?i - item ?p - person)
        :precondition (and (afternoon ?i)
                    (not (bodyOnTheClock ?p ?i)))
        :effect (bodyOnTheClock ?p ?i))

    (:action car_alarm
        :parameters (?clock - item ?p - person ?car - item)
        :precondition (alarm ?p ?car)
        :effect (and (afternoon ?clock)
                        (tower ?clock)
                        (existUnderTower ?car)))
)
