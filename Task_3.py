class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecturer(self, lecturer, course, grade):
        """
        Метод выставления оценки лектору.
        Условия:
        - Лектор должен быть закреплен за курсом, на который записан студент.
        - Оценка добавляется только в пределах от 1 до 10.
        """
        if (
            isinstance(lecturer, Lecturer)
            and course in self.courses_in_progress
            and course in lecturer.courses_attached
        ):
            if 1 <= grade <= 10:
                if course in lecturer.grades:
                    lecturer.grades[course].append(grade)
                else:
                    lecturer.grades[course] = [grade]
            else:
                return 'Ошибка: Оценка должна быть от 1 до 10'
        else:
            return 'Ошибка: Лектор не привязан к курсу или курс не в списке студента'

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)

    def get_average_grade(self):
        if not self.grades:
            return 0
        total_grades = sum(sum(grades) for grades in self.grades.values())
        num_grades = sum(len(grades) for grades in self.grades.values())
        return total_grades / num_grades if num_grades > 0 else 0

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


# Пример использования
best_student = Student('Ruoy', 'Eman', 'your_gender')
best_student.courses_in_progress += ['Python', 'Git']
best_student.finished_courses += ['Введение в программирование']

second_student = Student('John', 'Doe', 'male')
second_student.courses_in_progress += ['Python']

cool_lecturer = Lecturer('Some', 'Buddy')
cool_lecturer.courses_attached += ['Python']

another_lecturer = Lecturer('John', 'Smith')
another_lecturer.courses_attached += ['Python']

cool_reviewer = Reviewer('Anna', 'Ivanova')
cool_reviewer.courses_attached += ['Python']

cool_reviewer.rate_hw(best_student, 'Python', 10)
cool_reviewer.rate_hw(best_student, 'Python', 9)
cool_reviewer.rate_hw(second_student, 'Python', 8)

best_student.rate_lecturer(cool_lecturer, 'Python', 9)
best_student.rate_lecturer(cool_lecturer, 'Python', 10)
best_student.rate_lecturer(another_lecturer, 'Python', 8)

print("Студенты:")
print(best_student)
print(second_student)
print("\nЛекторы:")
print(cool_lecturer)
print(another_lecturer)
print("\nРевьюеры:")
print(cool_reviewer)

# Сравнение
print("\nСравнение студентов:")
print(best_student > second_student)  # True

print("\nСравнение лекторов:")
print(cool_lecturer > another_lecturer)  # True