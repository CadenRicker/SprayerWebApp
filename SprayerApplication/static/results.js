
$('select').on('change', function() {
  value = this.value;
  if (value == "Remove"){
  	$('#infectedDate').removeAttr('required');
  } 
  if (value != "Remove"){
  	$('#infectedDate').attr('required');
  	
  	
  }
});