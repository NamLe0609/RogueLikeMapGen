# Roguelike map generation

To start, run main.py from the gamefiles folder. To choose which type of map generation you want, press numbers from 1 to 5. Each number generates a map with the following algorithms:

1. Binary space partitioning (CASTLE/RECTANGULAR ROOMS)
2. Cellular automata (CAVERN)
3. Cellular automata (CATACOMBS)
4. Hybrid (OPEN SEWERS)
5. Hybrid (CLOSED SEWERS)
6. Binary space partitioning (MAZE)

Some generation methods are the same, but uses different configurations to generate different looking maps. Hybrids generation generates a map using BSP first, then applies CA to modify the layout. BSP (MAZE) uses a specific configuration that allows one tile wide corridors.
