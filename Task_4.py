class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)

    def get_average_grade(self):
        if not self.grades:
            return 0
        total_grades = sum(sum(grades) for grades in self.grades.values())
        num_grades = sum(len(grades) for grades in self.grades.values())
        return total_grades / num_grades if num_grades > 0 else 0

    def rate_lecturer(self, lecturer, course, grade):
        if (
            isinstance(lecturer, Lecturer)
            and course in self.courses_in_progress
            and course in lecturer.courses_attached
        ):
            if course in lecturer.grades:
                lecturer.grades[course].append(grade)
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        avg_grade = self.get_average_grade()
        courses_in_progress = ', '.join(self.courses_in_progress)
        finished_courses = ', '.join(self.finished_courses)
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за домашние задания: {avg_grade:.2f}\n"
            f"Курсы в процессе изучения: {courses_in_progress}\n"
            f"Завершенные курсы: {finished_courses}"
        )

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.get_average_grade() < other.get_average_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def get_average_grade(self):
        if not self.grades:
            return 0
        total_grades = sum(sum(grades) for grades in self.grades.values())
        num_grades = sum(len(grades) for grades in self.grades.values())
        return total_grades / num_grades if num_grades > 0 else 0

    def __str__(self):
        avg_grade = self.get_average_grade()
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за лекции: {avg_grade:.2f}"
        )

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.get_average_grade() < other.get_average_grade()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if (
            isinstance(student, Student)
            and course in self.courses_attached
            and course in student.courses_in_progress
        ):
            if course in student.grades:
                student.grades[course].append(grade)
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


# Функции подсчета средней оценки
def average_grade_students(students, course):
    total_grades = 0
    count = 0
    for student in students:
        if course in student.grades:
            total_grades += sum(student.grades[course])
            count += len(student.grades[course])
    return total_grades / count if count > 0 else 0


def average_grade_lecturers(lecturers, course):
    total_grades = 0
    count = 0
    for lecturer in lecturers:
        if course in lecturer.grades:
            total_grades += sum(lecturer.grades[course])
            count += len(lecturer.grades[course])
    return total_grades / count if count > 0 else 0


# Создание экземпляров
student1 = Student('Ruoy', 'Eman', 'male')
student1.courses_in_progress += ['Python']
student1.finished_courses += ['Git']

student2 = Student('Anna', 'Smith', 'female')
student2.courses_in_progress += ['Python']

lecturer1 = Lecturer('Some', 'Buddy')
lecturer1.courses_attached += ['Python']

lecturer2 = Lecturer('John', 'Doe')
lecturer2.courses_attached += ['Python']

reviewer1 = Reviewer('Paul', 'Reviewer')
reviewer1.courses_attached += ['Python']

reviewer2 = Reviewer('Kate', 'Reviewer')
reviewer2.courses_attached += ['Python']

# Выставление оценок студентам
reviewer1.rate_hw(student1, 'Python', 10)
reviewer1.rate_hw(student1, 'Python', 9)
reviewer2.rate_hw(student2, 'Python', 8)

# Студенты выставляют оценки лекторам
student1.rate_lecturer(lecturer1, 'Python', 9)
student1.rate_lecturer(lecturer1, 'Python', 10)
student2.rate_lecturer(lecturer2, 'Python', 8)
student2.rate_lecturer(lecturer2, 'Python', 9)

# Вывод данных
print(student1)
print(student2)
print(lecturer1)
print(lecturer2)
print(reviewer1)
print(reviewer2)

# Подсчет средних оценок
print("\nСредняя оценка за домашние задания по курсу Python:")
print(average_grade_students([student1, student2], 'Python'))

print("\nСредняя оценка за лекции по курсу Python:")
print(average_grade_lecturers([lecturer1, lecturer2], 'Python'))