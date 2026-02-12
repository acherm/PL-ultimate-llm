/**
* Simple predator-prey model in GAML
* Demonstrates basic agent-based modeling
*/

model PreyPredator

global {
    int number_of_prey <- 200;
    int number_of_predators <- 20;
    float prey_max_energy <- 1.0;
    float prey_energy_consum <- 0.05;
    float predator_max_energy <- 1.0;
    float predator_energy_consum <- 0.1;
    float prey_energy_from_food <- 0.1;
    float predator_energy_from_food <- 0.5;

    init {
        create prey number: number_of_prey;
        create predator number: number_of_predators;
    }
}

species prey {
    float energy <- rnd(prey_max_energy) update: energy - prey_energy_consum max: prey_max_energy;

    reflex eat when: vegetation_cell(location).food > 0 {
        float food_gain <- min([vegetation_cell(location).food, prey_energy_from_food]);
        vegetation_cell(location).food <- vegetation_cell(location).food - food_gain;
        energy <- energy + food_gain;
    }

    reflex move {
        do wander;
    }

    reflex reproduce when: energy >= prey_max_energy * 0.75 {
        create prey {
            location <- myself.location;
            energy <- myself.energy / 2;
        }
        energy <- energy / 2;
    }

    reflex die when: energy <= 0 {
        do die;
    }

    aspect default {
        draw circle(1) color: #blue;
    }
}

species predator {
    float energy <- rnd(predator_max_energy) update: energy - predator_energy_consum max: predator_max_energy;

    reflex eat when: !empty(prey at_distance 1) {
        ask one_of(prey at_distance 1) {
            do die;
        }
        energy <- energy + predator_energy_from_food;
    }

    reflex move {
        do wander;
    }

    reflex reproduce when: energy >= predator_max_energy * 0.75 {
        create predator {
            location <- myself.location;
            energy <- myself.energy / 2;
        }
        energy <- energy / 2;
    }

    reflex die when: energy <= 0 {
        do die;
    }

    aspect default {
        draw circle(2) color: #red;
    }
}

grid vegetation_cell width: 50 height: 50 {
    float food <- rnd(1.0) max: 1.0;

    reflex grow {
        food <- min([1.0, food + 0.01]);
    }

    aspect default {
        draw square(1) color: rgb(int(255 * (1 - food)), 255, int(255 * (1 - food)));
    }
}

experiment main type: gui {
    output {
        display map {
            grid vegetation_cell;
            species prey;
            species predator;
        }

        monitor "Prey" value: length(prey);
        monitor "Predators" value: length(predator);
    }
}
