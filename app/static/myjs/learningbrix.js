
//var service = 'http://localhost/DistributedDataSystem/Service.svc/';

 
$(document).ready(function(){
	
	$("#btnViewCourses").click(function(){
		
		var selected=$("#selectedClass").find(":selected").val();
		 //alert("Bingo  "+selected);
		 
		 var service = $SCRIPT_ROOT + '/getCourses';
		
			      $.getJSON(service, {
			        selectedClass: selected
			      }, function(data) {
			       alert(data.result);
			      });
			      return false;
			    
		 
	});
   

})
