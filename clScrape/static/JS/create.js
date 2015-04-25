/*Used to Create Make checkboxes*/
var make = ['Ford'];
/*Used to Create Model checkboxes*/
var model = ['F150','F-150','F250','F-250'];
/*Used to Create keyword checkboxes*/
var keywords = ['5.4L', '5.4 engine', 'needs', 'cam phasers', 
                'knock', 'needs work', 'needs engine', 
                'needs new engine', 'crew cab', 'crewcab'];

/*Used to build the page on load*/
function buildPage(){
  addItems('make', make);
  addItems('model', model);
  addItems('keywords', keywords);
  checkAll();
}

/*add elements to the page*/
function addItems(type, vals){
  var myModel = document.getElementById(type);
  var nameLabel = document.createElement('label');
  nameLabel.innerHTML = "<b>"+ type +"</b><br />";
  myModel.appendChild(nameLabel);
  
  for(var x=0; x<vals.length; x++){
    var makeLabel = document.createElement('label');
    makeLabel.innerHTML = vals[x];
    var makeCb = document.createElement("input");
    makeCb.name = vals[x];
    makeCb.id = vals[x];
    makeCb.value = type;
    makeCb.type = "checkbox";
    myModel.appendChild(makeLabel);
    myModel.appendChild(makeCb);
  }
  myModel.innerHTML += "<br /><br />";   
}

/*check all*/
function checkAll(){
  checkItems(make);
  checkItems(model);
  checkItems(keywords); 
}
function checkItems(vals){
  for(var x=0; x<vals.length; x++){
    document.getElementById(vals[x]).checked = true;
  }
}

/*uncheck all*/
function uncheckAll(){
  uncheckItems(make);
  uncheckItems(model);
  uncheckItems(keywords); 
}
function uncheckItems(vals){
  for(var x=0; x<vals.length; x++){
    document.getElementById(vals[x]).checked = false;
  }
}

/*Used to display Scrape Results*/
function displayData(formData){
  var results = document.getElementById('results');
  console.log(formData.hello);
  for(var x=0; x<formData.hello.length;x++){
    results.innerHTML += formData.hello[x];
  }
}