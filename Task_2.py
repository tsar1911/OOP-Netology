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

class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        avg_grade = self.get_average_grade()
        return f"Name: {self.name}\nSurname: {self.surname}\nAverage Grade: {avg_grade:.2f}"

    def get_average_grade(self):
        if not self.grades:
            return 0
        total_grades = sum(sum(grades) for grades in self.grades.values())
        num_grades = sum(len(grades) for grades in self.grades.values())
        return total_grades / num_grades if num_grades > 0 else 0

class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        """
        Метод выставления оценки студенту за домашнюю работу.
        Условия:
        - Студент должен быть записан на курс.
        - Курс должен быть закреплен за проверяющим.
        """
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course].append(grade)
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f"Name: {self.name}\nSurname: {self.surname}"

# Пример использования
best_student = Student('Ruoy', 'Eman', 'your_gender')
best_student.courses_in_progress += ['Python']

cool_reviewer = Reviewer('Some', 'Buddy')
cool_reviewer.courses_attached += ['Python']

cool_lecturer = Lecturer('John', 'Doe')
cool_lecturer.courses_attached += ['Python']

# Выставляем оценки студенту
cool_reviewer.rate_hw(best_student, 'Python', 9)
cool_reviewer.rate_hw(best_student, 'Python', 10)

# Студент выставляет оценки лектору
best_student.rate_lecturer(cool_lecturer, 'Python', 10)
best_student.rate_lecturer(cool_lecturer, 'Python', 9)

# Вывод результатов
print("Student grades:")
print(best_student.grades)
print("\nReviewer:")
print(cool_reviewer)
print("\nLecturer:")
print(cool_lecturer)