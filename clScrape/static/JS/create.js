function buildPage(){
  var make = ['Ford'];
  var model = ['F150','F-150','F250','F-250'];
  var keywords = ['5.4L', '5.4 engine', 'needs', 'cam phasers', 
                  'knock', 'needs work', 'needs engine', 'needs new engine'];
  
  addItems('make', make);
  addItems('model', model);
  addItems('keywords', keywords);
  
  checkItems(make);
  checkItems(model);
  checkItems(keywords);  
}

function addItems(type, vals){
  var myModel = document.getElementById(type);
  var nameLabel = document.createElement('label');
  nameLabel.innerHTML = "<b>"+ type +"</b><br />";
  myModel.appendChild(nameLabel);
  
  for(var x=0; x<vals.length; x++){
    var makeLabel = document.createElement('label');
    makeLabel.innerHTML = vals[x];
    var makeCb = document.createElement("input");
    makeCb.id = vals[x];
    makeCb.value = vals[x];
    makeCb.type = "checkbox";
    myModel.appendChild(makeLabel);
    myModel.appendChild(makeCb);
  }
  myModel.innerHTML += "<br /><br />";   
}

function checkItems(vals){
  for(var x=0; x<vals.length; x++){
    document.getElementById(vals[x]).checked = true;
  }
}

function displayData(clData){
  //var results = document.getElementById('results');
  console.log("HELLO");
  console.log(clData);
  console.log("GBYE");
  //results.innerHTML += clData;
}