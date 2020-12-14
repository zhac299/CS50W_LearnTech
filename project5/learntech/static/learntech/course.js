var ID;
var theCourse = "";
var theUser = "";

document.addEventListener('DOMContentLoaded', function() {    
    ID = document.querySelector('#course-id').value;

    const leaveCourse = document.createElement('div');
    leaveCourse.innerHTML = `<button class="btn btn-warning">Leave Course</button>`;
    document.querySelector(`#but-div`).append(leaveCourse);    

    document.addEventListener('click', event => {
        const element = event.target;

        if (element.className == 'btn btn-warning') {            
            getCourseFromID(ID);
            unenrollCourse(ID);
            location.href="/"
        }
    })

})

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

function unenrollCourse(courseID) {
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