document.addEventListener('DOMContentLoaded', function() {
    var isTeacherCheck = document.querySelector('#is-user-teacher').value;

    document.querySelector('#show-enrolled').addEventListener('click', () => {
        if (isTeacherCheck == "True") {
            document.querySelector('#taught-div').innerHTML = '';
        }

        document.querySelector('#course-div').innerHTML = `<h2>Courses I'm Enrolled in:</h2>`;

        load_user_courses();
    })

    if (isTeacherCheck == "True") {

        document.querySelector('#show-taught').addEventListener('click', () => {
            document.querySelector('#course-div').innerHTML = '';
    
            document.querySelector('#taught-div').innerHTML = `<h2>Courses I Teach:</h2>`;
    
            load_taught_courses();
        });
    
    }
})

function load_user_courses() {
    fetch('/getEnrolledCourse')
    .then(response => response.json())
    .then(allCourses => {
        allCourses.forEach(function(item) {         
            const theCourse = document.createElement('div');
            theCourse.style = 'border-style: solid';
            theCourse.innerHTML = `<div id="course-${item.id}" style="border-style: groove"><a href="../course/${item.id}">${item.courseName}</a><p></p> by <a href="/profile/${item.courseTeacher}">${item.courseTeacher}</a></div>`;
            document.querySelector('#course-div').append(theCourse);
        });
    });
} 

function load_taught_courses() {
    fetch('/getTaughtCourse')
    .then(response => response.json())
    .then(allCourses => {
        allCourses.forEach(function(item) {         
            const theCourse = document.createElement('div');
            theCourse.style = 'border-style: solid';
            theCourse.innerHTML = `<div id="course-${item.id}" style="border-style: groove"><a href="../course/${item.id}">${item.courseName}</a><p></p> by <a href="/profile/${item.courseTeacher}">${item.courseTeacher}</a></div>`;
            document.querySelector('#taught-div').append(theCourse);
        });
    });
} 