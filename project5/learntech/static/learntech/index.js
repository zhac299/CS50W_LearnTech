var theCourse = "";
var theUser = "";

document.addEventListener('DOMContentLoaded', function() {    
    load_all_courses();

    document.addEventListener('click', event => {
        const element = event.target;

        if (element.className == 'btn btn-secondary') {            
            var courseID = element.name;
            getCourseFromID(courseID);

            getEditView(courseID)            
        }
    })

    document.addEventListener('click', event => {
        const element = event.target;

        if (element.className == 'btn btn-info') {   
            var courseID = element.name;
         
            edit(courseID)
        }
    })

    document.addEventListener('click', event => {
        const element = event.target;

        if (element.className == 'btn btn-dark') {   
            var courseID = element.name;
            console.log(courseID)
         
            getCourseFromID(courseID);
            joinCourse(courseID);
        }
    })

    document.addEventListener('click', event => {
        const element = event.target;

        if (element.className == 'btn btn-warning') {   
            var courseID = element.name;
         
            getCourseFromID(courseID);
            leaveCourse(courseID);
        }
    })
})

function load_all_courses() {
    currentUser = document.querySelector('#loggedInUserID').value;

    fetch('/getCourse')
    .then(response => response.json())
    .then(allCourses => {
        allCourses.forEach(function(item) {         
            const theCourse = document.createElement('div');
            theCourse.style = 'border-style: solid';
            theCourse.innerHTML = `<div id="course-${item.id}" style="border-style: groove">${item.courseName}<p></p> by <a href="/profile/${item.courseTeacher}">${item.courseTeacher}</a> <p></p> Currently Enrolled : ${item.currentlyEnrolled}<br></br></div>`;
            document.querySelector('#course-content').append(theCourse);

            const joinCourse = document.createElement('div');
            joinCourse.innerHTML = `<input name="${item.id}" type="submit" class="btn btn-dark" value="Enroll">`;
            document.querySelector(`#course-${item.id}`).append(joinCourse);    

            const leaveCourse = document.createElement('div');
            leaveCourse.innerHTML = `<button name="${item.id}" class="btn btn-warning">Leave Course</button>`;
            document.querySelector(`#course-${item.id}`).append(leaveCourse);    

            if (currentUser == item.courseTeacher) {
                const updateButton = document.createElement('div');
                updateButton.className = 'update';
                updateButton.innerHTML =`<button id="update-button" name="${item.id}" class="btn btn-secondary">Edit</button>`;
                document.querySelector(`#course-${item.id}`).append(updateButton);
            }
        });
    });
} 

function getCourseFromID(courseID) {
    fetch('/getID/'+courseID)
    .then(response => response.json())
    .then(allFollowing => {
        allFollowing.forEach(function(item) {

            if (item.id == courseID) {
                theCourse = item;
                theUser = item.user;
            }
            
        });
    });
}

function joinCourse(courseID) {
    fetch('/joinCourse/'+courseID, {
        method: 'POST',
        body: JSON.stringify({
            studentName: theUser,
            course: theCourse
        })
      })
      .then(response => response.json())
      .then(result => {
        // Print result
        console.log(result);    
      })
}

function leaveCourse(courseID) {
    fetch('/leaveCourse/'+courseID, {
        method: 'POST',
        body: JSON.stringify({
            studentName: theUser,
            course: theCourse
        })
      })
      .then(response => response.json())
      .then(result => {
          // Print result
          console.log(result);
      })
}

function getEditView(theID) {
    fetch('/editPost/'+theID)
    .then(response => response.json())
    .then(allFollowing => {
        allFollowing.forEach(function(item) {
            const EditPost = document.createElement('div');
            EditPost.id = 'edit-div';
            EditPost.style = 'border-style: dotted';
            EditPost.innerHTML = `<textarea class="form-control" id="edit-textarea" rows="5">${item.courseData}</textarea>`;
            document.querySelector(`#course-${theID}`).append(EditPost);
            
            const updateButDiv = document.createElement('div');
            updateButDiv.id = 'update-div';
            updateButDiv.innerHTML = `<div><input name=${theID} id="update-${theID}" class="btn btn-info" type="submit" value="Update"></input></div>`;            
            document.querySelector(`#course-${theID}`).append(updateButDiv);    
        });
    });
}

function edit(theID) {
    fetch('/editUpdate/'+theID, {
        method: 'PUT',
        body: JSON.stringify({
            courseData: document.querySelector('#edit-textarea').value
        })
      });      
}