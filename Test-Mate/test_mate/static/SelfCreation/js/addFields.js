// FIRST TIME DISPLAY INTERACTION.

// QUESTION

var firstTime = document.getElementById('first');
firstTime.oninput = qFunc;

function qFunc(e) {
  var disp = document.getElementById('time_1');
  disp.innerHTML = e.target.value;
}

// POSITIVES

var posfirst = document.getElementById('posFirst');
posfirst.oninput = pFunc;

function pFunc(e){
  var disp = document.getElementById('posFirst_1');
  disp.innerHTML = e.target.value;
}

// NEGATIVES

var negfirst = document.getElementById('negFirst');
negfirst.oninput = nFunc;

function nFunc(e){
  var disp = document.getElementById('negFirst_1');
  disp.innerHTML = e.target.value;
}


// DURATION

var dur = document.getElementById('duration');
dur.oninput = dFunc;

function dFunc(e){
  var disp = document.getElementById('duration_');
  disp.innerHTML = e.target.value;
}

/* Below is the code to dynamically add the fields of our choice. - {negative,positive,questions - SECTION-WISE} */

//slider alteration for question section.
function funQuestion(e){
   var disp = document.getElementById('quantity_'+parseInt(e.target.id));
   disp.innerHTML = e.target.value;
}

//slider alteration for Positives section.
function funPositive(e){
   var disp = document.getElementById('pos_'+parseInt(e.target.id));
   disp.innerHTML = e.target.value;
}

//slider alteration for Negatives section.
function funNegative(e){
   var disp = document.getElementById('neg_'+parseInt(e.target.id));
   disp.innerHTML = e.target.value;
}


// FOR SECTION'S QUESTIONS,SECTION'S NEGATIVE, SECTION'S POSITIVE.

function addField(elem){
  var numberOfFields = parseInt(elem.getAttribute('value'));

  var question_container = document.getElementById("question-Sections");
  var pos_container = document.getElementById("positive-Sections");
  var neg_container = document.getElementById("negative-Sections");


  while (question_container.hasChildNodes()){
      question_container.removeChild(question_container.lastChild);
  }

  while(pos_container.hasChildNodes()){
      pos_container.removeChild(pos_container.lastChild);
  }

  while(neg_container.hasChildNodes()){
      neg_container.removeChild(neg_container.lastChild);
  }

  //add new content in question container
  for(var i=0;i<numberOfFields;i++){

    var outerContainer = document.createElement("div");
    outerContainer.className = "row";
    outerContainer.style = "margin-right: 0px;";

    // Part-1 Text Part
    var innerContainer1_1 = document.createElement('div');
    innerContainer1_1.className = "col-sm";
    innerContainer1_1.style = "margin-top: 30px;"

    var innerContainer1_2 = document.createElement('label');
    innerContainer1_2.setAttribute("for",(i+1)+"_quantity");
    innerContainer1_2.appendChild(document.createTextNode("Section - "+(i+1)+" :"));

    innerContainer1_1.appendChild(innerContainer1_2);
    outerContainer.appendChild(innerContainer1_1);

    // Part-2 Slider Part
    var innerContainer2_1 = document.createElement('div');
    innerContainer2_1.style = "bottom: 35px;padding-left:0px;padding-right:0px;";
    innerContainer2_1.className = "col-sm";

    var innerContainer2_2 = document.createElement('div');
    innerContainer2_2.className = "range-slider";

    var innerContainer2_3_1 = document.createElement('input');
    innerContainer2_3_1.className = "range-slider__range";
    innerContainer2_3_1.id = (i+1)+"_quantity";
    innerContainer2_3_1.type="range";
    innerContainer2_3_1.setAttribute("value","10");
    innerContainer2_3_1.name="numberOfQuestion_"+(i+1);
    innerContainer2_3_1.min="2";
    innerContainer2_3_1.max="15";

    var innerContainer2_3_2 = document.createElement('span');
    innerContainer2_3_2.className = "range-slider__value";
    innerContainer2_3_2.classList.add('disp_'+(i+1));
    innerContainer2_3_2.id = "quantity_"+(i+1);
    innerContainer2_3_2.innerHTML = innerContainer2_3_1.value;

    innerContainer2_2.appendChild(innerContainer2_3_1);
    innerContainer2_2.appendChild(innerContainer2_3_2);
    innerContainer2_1.appendChild(innerContainer2_2);
    outerContainer.appendChild(innerContainer2_1);

    question_container.appendChild(outerContainer);
    question_container.appendChild(document.createElement('hr'));

    var out = document.getElementById((i+1)+'_quantity');
    out.oninput = funQuestion;
  }

  //add new content in positive container
  for(var i=0;i<numberOfFields;i++){

    var outerContainer = document.createElement("div");
    outerContainer.className = "row";
    outerContainer.style = "margin-right: 0px;";

    // Part-1 Text Part
    var innerContainer1_1 = document.createElement('div');
    innerContainer1_1.className = "col-sm";
    innerContainer1_1.style = "margin-top: 30px;"

    var innerContainer1_2 = document.createElement('label');
    innerContainer1_2.setAttribute("for",(i+1)+"_pos");
    innerContainer1_2.appendChild(document.createTextNode("Section - "+(i+1)+" :"));

    innerContainer1_1.appendChild(innerContainer1_2);
    outerContainer.appendChild(innerContainer1_1);

    // Part-2 Slider Part
    var innerContainer2_1 = document.createElement('div');
    innerContainer2_1.style = "bottom: 35px;padding-left:0px;padding-right:0px;";
    innerContainer2_1.className = "col-sm";

    var innerContainer2_2 = document.createElement('div');
    innerContainer2_2.className = "range-slider";

    var innerContainer2_3_1 = document.createElement('input');
    innerContainer2_3_1.className = "range-slider__range";
    innerContainer2_3_1.id = (i+1)+"_pos";
    innerContainer2_3_1.type="range";
    innerContainer2_3_1.setAttribute("value","3");
    innerContainer2_3_1.name="pos_"+(i+1);
    innerContainer2_3_1.min="1";
    innerContainer2_3_1.max="10";

    var innerContainer2_3_2 = document.createElement('span');
    innerContainer2_3_2.className = "range-slider__value";
    innerContainer2_3_2.classList.add('disp_'+(i+1));
    innerContainer2_3_2.id = "pos_"+(i+1);
    innerContainer2_3_2.innerHTML = innerContainer2_3_1.value;

    innerContainer2_2.appendChild(innerContainer2_3_1);
    innerContainer2_2.appendChild(innerContainer2_3_2);
    innerContainer2_1.appendChild(innerContainer2_2);
    outerContainer.appendChild(innerContainer2_1);

    pos_container.appendChild(outerContainer);
    pos_container.appendChild(document.createElement('hr'));

    var out = document.getElementById((i+1)+'_pos');
    out.oninput = funPositive;
  }

  //add new content in negative container
  for(var i=0;i<numberOfFields;i++){

    var outerContainer = document.createElement("div");
    outerContainer.className = "row";
    outerContainer.style = "margin-right: 0px;";

    // Part-1 Text Part
    var innerContainer1_1 = document.createElement('div');
    innerContainer1_1.className = "col-sm";
    innerContainer1_1.style = "margin-top: 30px;"

    var innerContainer1_2 = document.createElement('label');
    innerContainer1_2.setAttribute("for",(i+1)+"_neg");
    innerContainer1_2.appendChild(document.createTextNode("Section - "+(i+1)+" :"));

    innerContainer1_1.appendChild(innerContainer1_2);
    outerContainer.appendChild(innerContainer1_1);

    // Part-2 Slider Part
    var innerContainer2_1 = document.createElement('div');
    innerContainer2_1.style = "bottom: 35px;padding-left:0px;padding-right:0px;";
    innerContainer2_1.className = "col-sm";

    var innerContainer2_2 = document.createElement('div');
    innerContainer2_2.className = "range-slider";

    var innerContainer2_3_1 = document.createElement('input');
    innerContainer2_3_1.className = "range-slider__range";
    innerContainer2_3_1.id = (i+1)+"_neg";
    innerContainer2_3_1.type="range";
    innerContainer2_3_1.setAttribute("value","-1");
    innerContainer2_3_1.name="neg_"+(i+1);
    innerContainer2_3_1.min="-4";
    innerContainer2_3_1.max="0";

    var innerContainer2_3_2 = document.createElement('span');
    innerContainer2_3_2.className = "range-slider__value";
    innerContainer2_3_2.classList.add('disp_'+(i+1));
    innerContainer2_3_2.id = "neg_"+(i+1);
    innerContainer2_3_2.innerHTML = innerContainer2_3_1.value;

    innerContainer2_2.appendChild(innerContainer2_3_1);
    innerContainer2_2.appendChild(innerContainer2_3_2);
    innerContainer2_1.appendChild(innerContainer2_2);
    outerContainer.appendChild(innerContainer2_1);

    neg_container.appendChild(outerContainer);
    neg_container.appendChild(document.createElement('hr'));

    var out = document.getElementById((i+1)+'_neg');
    out.oninput = funNegative;
  }
}
