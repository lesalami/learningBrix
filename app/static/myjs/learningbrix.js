//var service = 'http://localhost/DistributedDataSystem/Service.svc/';


$(document).ready(function() {

    $("#divGrades").hide();

    $("#btnViewCourses").click(function() {

        var selected = $("#selectedClass").find(":selected").val();
          var selectedText = $("#selectedClass").find(":selected").text();
        //alert("Bingo  "+selected);

        var student_id = $("#studentID").val();

        var service = $SCRIPT_ROOT + '/getCourses';

        $.getJSON(service, {
            selectedClass: selected,
            student_id: student_id

        }, function(data) {

            //alert(data);
            console.log(data);

            str = "<tr><th>Course</th><th>Grade</th></tr>";

            for (var i = 0; i < data.courses.length; i++) {

                var course = data.courses[i];
                var value = 0;
                if ("value" in course) {
                    value = course.value;
                } else {
                    value = 0;
                }

                str += '<tr><td>' + course.name + '</td>' + '<td><input class="txtCourses" type="text" id="' + course.name + '" value="' + value + '" /></td></tr>';

            }


            $("#schoolID").val(data.school_id);
            $("#curriculumID").val(data.curriculum_id);
            $("#classID").val(data.class_id);

            $("#tblGrades").html(str);
            $("#divGrades").show();
            $("#classStatus").html('Enter grades for class '+selectedText);

        });
        return false;


    });




    $("#btnSaveGrades").click(function() {

        var school_id = $("#schoolID").val();
        var curriculum_id = $("#curriculumID").val();
        var class_id = $("#classID").val();
        var student_id = $("#studentID").val();

        var dictGradedCourses = []; // create an empty array

        var service = $SCRIPT_ROOT + '/saveGrades';

        $(".txtCourses").each(function() {

            //alert($(this).attr('id') + " " + $(this).val());

            dictGradedCourses.push({
                key: $(this).attr('id'),
                value: $(this).val()
            });
        });

        var jsonData = JSON.stringify([{
            school_id: school_id,
            curriculum_id: curriculum_id,
            class_id: class_id,
            student_id: student_id,
            gradedCourses: dictGradedCourses
        }]);

        $.ajax({
            type: "POST",
            url: service,

            contentType: "application/json; charset=utf-8",

            data: jsonData,
            success: function(data) {
            
            
            
                $("#ajax-alert").toggleClass('alert alert-success alert-dismissable');
                $("#ajax-alert").html('<button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button> Grades have been saved successfully!');

            },
            failure: function(errMsg) {
                $("#ajax-alert").toggleClass('alert alert-danger alert-dismissable');
                $("#ajax-alert").html('<button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button> Grades was not saved!: '+errMsg);

            }


        });


    });


});