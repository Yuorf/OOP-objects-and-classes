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

    def rate_lecturer(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def average_grade(self):
        all_grades = [grade for grades in self.grades.values() for grade in grades]
        if not all_grades:
            return 0
        return sum(all_grades) / len(all_grades)

    def __str__(self):
        avg_grade = self.average_grade()
        courses_in_progress = ", ".join(self.courses_in_progress)
        finished_courses = ", ".join(self.finished_courses)
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}\n"
                f"Средняя оценка за домашние задания: {avg_grade:.2f}\n"
                f"Курсы в процессе изучения: {courses_in_progress}\n"
                f"Завершенные курсы: {finished_courses}")

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_grade() < other.average_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def average_grade(self):
        all_grades = [grade for grades in self.grades.values() for grade in grades]
        if not all_grades:
            return 0
        return sum(all_grades) / len(all_grades)

    def __str__(self):
        avg_grade = self.average_grade()
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}\n"
                f"Средняя оценка за лекции: {avg_grade:.2f}")

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_grade() < other.average_grade()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


def average_grade_for_course(students, course):
    total_grades = []
    for student in students:
        if course in student.grades:
            total_grades.extend(student.grades[course])
    if not total_grades:
        return 0
    return sum(total_grades) / len(total_grades)


def average_lecturer_grade_for_course(lecturers, course):
    total_grades = []
    for lecturer in lecturers:
        if course in lecturer.grades:
            total_grades.extend(lecturer.grades[course])
    if not total_grades:
        return 0
    return sum(total_grades) / len(total_grades)


student1 = Student('Tema', 'Shchelupanov', 'men')
student1.courses_in_progress.append('Python')
student2 = Student('Victor', 'Coy', 'men')
student2.courses_in_progress.append('Python')
lecturer1 = Lecturer('Alexsandra', 'Ismailova')
lecturer1.courses_attached.append('Python')
lecturer2 = Lecturer('Ivan', 'Ivanov')
lecturer2.courses_attached.append('Python')
reviewer = Reviewer('Some', 'Buddy')
reviewer.courses_attached.append('Python')
reviewer.rate_hw(student1, 'Python', 10)
reviewer.rate_hw(student1, 'Python', 9)
reviewer.rate_hw(student2, 'Python', 8)
student1.rate_lecturer(lecturer1, 'Python', 10)
student1.rate_lecturer(lecturer2, 'Python', 8)

print(student1)
print(lecturer1)
print(reviewer)
print(average_grade_for_course([student1, student2], 'Python'))
print(average_lecturer_grade_for_course([lecturer1, lecturer2], 'Python'))