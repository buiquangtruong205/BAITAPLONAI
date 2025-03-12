import numpy as np

# Mã hóa mối quan hệ giữa khách mời
relationship_scores = {
    'spouse': 2000,
    'sibling': 900,
    'parent_child': 700,
    'cousin': 500,
    'uncle_aunt_nephew_niece': 300,
    'friend': 100,
    'unknown': 0
}

# Hàm tính điểm thân thiết của một bàn
def table_score(table, relationships):
    score = 0
    for i in range(len(table)):
        for j in range(i + 1, len(table)):
            score += relationships[table[i]].get(table[j], 0)
    return score

# Hàm fitness: tính tổng điểm thân thiết của tất cả các bàn
def fitness_function(seating, relationships, max_table_size):
    total_score = 0
    for table in seating:
        if len(table) <= max_table_size:
            total_score += table_score(table, relationships)
    return total_score

# Khởi tạo quần thể
def initialize_population(pop_size, guests, num_tables):
    population = []
    for _ in range(pop_size):
        np.random.shuffle(guests)
        seating = [guests[i::num_tables] for i in range(num_tables)]
        population.append(seating)
    return population

# Tính toán độ thích nghi của quần thể
def calculate_fitness(population, relationships, max_table_size):
    fitness = [fitness_function(seating, relationships, max_table_size) for seating in population]
    return fitness

# Chọn lọc
def selection(population, fitness):
    total_fitness = np.sum(fitness)
    probabilities = fitness / total_fitness
    indices = np.random.choice(len(fitness), size=len(fitness), p=probabilities)
    selected_population = [population[i] for i in indices]
    return selected_population

# Lai ghép
def crossover(parents, crossover_rate):
    offspring = []
    for i in range(0, len(parents), 2):
        if i + 1 < len(parents) and np.random.rand() < crossover_rate:
            cut = np.random.randint(1, len(parents[i]))
            child1 = parents[i][:cut] + parents[i+1][cut:]
            child2 = parents[i+1][:cut] + parents[i][cut:]
            offspring.extend([child1, child2])
        else:
            offspring.extend([parents[i], parents[i+1]])
    return offspring

# Đột biến
def mutation(offspring, mutation_rate, guests, num_tables):
    for seating in offspring:
        if np.random.rand() < mutation_rate:
            table1, table2 = np.random.choice(len(seating), 2, replace=False)
            guest1, guest2 = np.random.choice(len(seating[table1]), 1)[0], np.random.choice(len(seating[table2]), 1)[0]
            seating[table1][guest1], seating[table2][guest2] = seating[table2][guest2], seating[table1][guest1]
    return offspring

# Thuật toán di truyền
def genetic_algorithm(pop_size, guests, num_tables, relationships, max_table_size, crossover_rate, mutation_rate, n_generations):
    population = initialize_population(pop_size, guests, num_tables)
    for generation in range(n_generations):
        fitness = calculate_fitness(population, relationships, max_table_size)
        print(f"Generation {generation}: Best fitness = {max(fitness)}, Average fitness = {np.mean(fitness)}")
        parents = selection(population, fitness)
        offspring = crossover(parents, crossover_rate)
        population = mutation(offspring, mutation_rate, guests, num_tables)
    
    # Tìm sơ đồ sắp xếp tốt nhất
    fitness = calculate_fitness(population, relationships, max_table_size)
    best_index = np.argmax(fitness)
    best_seating = population[best_index]
    best_fitness = fitness[best_index]

    return best_seating, best_fitness

# Nhập số lượng khách mời
num_guests = int(input("Nhập số lượng khách mời: "))
guests = [f'Guest{i+1}' for i in range(num_guests)]

# Nhập số lượng bàn
num_tables = int(input("Nhập số lượng bàn: "))

# Nhập kích thước tối đa của mỗi bàn
max_table_size = int(input("Nhập kích thước tối đa của mỗi bàn: "))

# Ví dụ về mối quan hệ giữa các khách mời (có thể thay đổi tùy theo yêu cầu)
relationships = {guest: {other_guest: np.random.choice(list(relationship_scores.values())) for other_guest in guests if other_guest != guest} for guest in guests}

# Các tham số của thuật toán di truyền
pop_size = 20
crossover_rate = 0.8
mutation_rate = 0.1
n_generations = 100 # số bước lặp

# Chạy thuật toán di truyền
best_seating, best_fitness = genetic_algorithm(pop_size, guests, num_tables, relationships, max_table_size, crossover_rate, mutation_rate, n_generations)

# In ra kết quả
print(f"Sơ đồ sắp xếp tốt nhất: {best_seating}")
print(f"Điểm thân thiết cao nhất: {best_fitness}")

# In ra danh sách khách mời trong từng bàn
for i, table in enumerate(best_seating):
    print(f"Bàn {i+1}: {', '.join(table)}")