var viewPanel
var starArray = new Array()
var controlKit
var helpDisplayed = false
var colormapDisplayed =  false

porthole.connected = function() {
    {{py print "started porthole connected function"}}
    controlKit = new ControlKit();
    controlKit.addPanel({label: 'Star Group Settings' , fixed: false, width: 320,position: [window.innerWidth -  320, 50]});
    console.log(controlKit)
    viewPanel = controlKit._panels[0]
    console.log(viewPanel)
    //$('#helpBox').dialog('close');

    $('#colormapPreview').dialog('close');
    helpDisplayed = true 
    colormapDisplayed = false
}

var numStarPanels = 0
var currentColors = new Array()
var currentFilterSettings = new Array()
var currentColorSettings = new Array()
var currentVariableColor = new Array(10)
var currentVariableFilter = new Array(10)
var groupNames = new Array(10)
var colorMapLabels = new Array(10)
var colorMapArray = new Array(10)
var variableArray = new Array(10)
var variableRanges = new Array(10)
var colorMapPaths = new Array(10)
var consoleString = ""

function setColorMapArrays( cm, cml,cp) {
    colorMapArray = cm
    colorMapLabels = cml
    colorMapPaths = cp
}
function setVariables( variables, ranges) {
    console.log("Variables Set")
    variableArray = variables
    variableRanges = ranges
}
function printConsole(text) {
    text = "Another line of Text"
    consoleString = consoleString + "<BR>" + text
    $("#consoleText").html(consoleString)
    $('#console').animate({
        scrollTop: $('#console').scrollTop() + $('#console').height()
    });
}
function setConsole(text) {
    $("#consoleText").html(text)
}
function clearConsole(text) {
    consoleString = ""
    $("#consoleText").html(consoleString)
}

function toggleHelp() {
    if (helpDisplayed) {
        $('#helpBox').dialog('close');
    } else {
        $('#helpBox').dialog('open');
    }
    //helpDisplayed = ! helpDisplayed 

}

function  toggleColorMap() {
    if (colormapDisplayed) {
        $('#colormapPreview').dialog('close');
    } else {
        $('#colormapPreview').dialog('open');
    }
    //colormapDisplayed = ! colormapDisplayed 
}

function addStarPanel(name, variables, ranges ) {
    {{py print "Adding a new Star Panel"}}
    console.log(variables)
    console.log(ranges)
    console.log(name)
    var obj = {
        colorRange : [0.0,100.0],
        colorAreaRange : [0.0,100.0],
        filterRange : [0.0,100.0],
        colorArea : 50,
        colorAreaStr : "50",
        colorCenter : 50,
        filterCenter : 50,
        filterAreaRange : [0.0,100.0],
        filterArea : 50,
        filterAreaStr : "50",
        filterOn: false,
        isLog: false,
        variables : variables,
        colors : colorMapLabels,
        val1 : 0,
        val2 : 0
    };
    starArray.push(obj)
    groupNames[numStarPanels] = name
    currentFilterSettings[numStarPanels] = new Array(10)
    currentFilterSettings[numStarPanels].fill(0)
    currentColorSettings[numStarPanels] = new Array(10)
    currentColorSettings[numStarPanels].fill(0)

    var currIndex = numStarPanels
    viewPanel.addGroup({label: name, enable: false})
        .addSubGroup({label: 'Color Settings', enable: false})
            .addSelect(starArray[numStarPanels], 'variables' , {label: 'Variable', onChange: function (index) {
                updateTables()
                $("#cColorvariable").html(variableArray[index])
                currentVariableColor[currIndex] = index
                if (currentColorSettings[currIndex][index] == 0) {
                    currentColorSettings[currIndex][index]= {
                        on : false,
                        min : ranges[index][0],
                        max : ranges[index][1]
                    }
                    starArray[currIndex].isLog = currentColorSettings[currIndex][index].ons
                    starArray[currIndex].colorRange = [currentColorSettings[currIndex][index].min, currentColorSettings[currIndex][index].max]
                } else {
                    starArray[currIndex].isLog = currentColorSettings[currIndex][index].on
                    starArray[currIndex].colorRange = [currentColorSettings[currIndex][index].min, currentColorSettings[currIndex][index].max]
                }
                controlKit.update();
                {{py setColorVariable("%starArray[currIndex].variables[index]%","%groupNames[currIndex]%")}}
            }})
            .addSelect(starArray[numStarPanels], 'colors', {label: 'Colors', onChange: function (index) {
                console.log('color map changed')
                {{py setColorMap("%colorMapArray[index]%","%groupNames[currIndex]%")}}
                $("#colorMapImg").attr('src',colorMapPaths[index]);
            }})
            //.addRange(starArray[numStarPanels],'colorRange',{label : 'Range:'})
            .addCheckbox(starArray[numStarPanels], 'isLog', {label: 'Log Scale'})

            .addSlider(starArray[numStarPanels],'colorCenter','colorRange',{label : 'Color Center:', dp: 20})
            .addSlider(starArray[numStarPanels],'colorArea','colorAreaRange',{label : 'Color Range:', dp: 20})
            .addStringInput(starArray[numStarPanels],'colorAreaStr',{ label: 'Range Max', // replace key label with custom one
                                    onChange : function(){  // on enter
                                        starArray[currIndex].colorAreaRange[1] = parseFloat(starArray[currIndex].colorAreaStr)
                                        console.log(starArray[currIndex].colorAreaStr)
                                    }
                                  })
            .addButton('Reset Filters',function(){
                    starArray[currIndex].colorAreaRange[0] = 0
                    starArray[currIndex].colorAreaRange[1] = 100
                    starArray[currIndex].colorCenter = 50
                    starArray[currIndex].colorArea = 50
                }, {})
        .addSubGroup({label: 'Filter Settings', enable: false})
            .addSelect(starArray[numStarPanels], 'variables', {label: 'Variable', onChange: function (index) {
                updateTables()
                currentVariableFilter[currIndex] = index
                if (currentFilterSettings[currIndex][index] == 0) {
                    console.log('new')
                    currentFilterSettings[currIndex][index]= {
                        on : false,
                        min : 0.0,
                        max : 1.0
                    }
                    starArray[currIndex].filterOn = currentFilterSettings[currIndex][index].on
                    starArray[currIndex].filterRange = [currentFilterSettings[currIndex][index].min, currentFilterSettings[currIndex][index].max]
                } else {
                    starArray[currIndex].filterOn = currentFilterSettings[currIndex][index].on
                    starArray[currIndex].filterRange = [currentFilterSettings[currIndex][index].min, currentFilterSettings[currIndex][index].max]
                    //console.log(starArray[currIndex].filterOn)
                }
                // obj.funcTarget = obj.funcs[index];
                starArray[currIndex].filterRange = variableRanges[index]
                controlKit.update();
            }})
            .addCheckbox(starArray[numStarPanels], 'filterOn', {label: 'Filter On'})
            .addSlider(starArray[numStarPanels],'filterCenter','filterRange',{label : 'Filter Center:', dp: 20})
            .addSlider(starArray[numStarPanels],'filterArea','filterAreaRange',{label : 'Filter Range:', dp: 20})
            .addStringInput(starArray[numStarPanels],'filterAreaStr',{ label: 'Range Max', // replace key label with custom one
                                    onChange : function(){  // on enter
                                        starArray[currIndex].filterAreaRange[1] = parseFloat(starArray[currIndex].filterAreaStr)
                                        console.log("Filter Max Area: ", starArray[currIndex].filterAreaRange[1])
                                    }
                                  })
            .addButton('Reset Filters',function(){
                    starArray[currIndex].filterAreaRange[0] = 0
                    starArray[currIndex].filterAreaRange[1] = 100
                    starArray[currIndex].filterCenter = 50
                    starArray[currIndex].filterArea = 50
                }, {})
        .addSubGroup({label: 'Information'})
            .addNumberOutput(starArray[numStarPanels], 'val1', {label: 'Val 1:'})
            .addNumberOutput(starArray[numStarPanels], 'val2', {label: 'Val 2:'})
    {{py print "Now done"}}
    numStarPanels = numStarPanels + 1
}


// controlKit.update();
function update(){
    for (var i = currentFilterSettings.length - 1; i >= 0; i--) {    // Loop through all current sets.
        //{{py setColorRange(%starArray[i].colorRange[0]%, %starArray[i].colorRange[1]%,"%groupNames[i]%")}}
        var min = starArray[i].colorCenter - starArray[i].colorArea
        var max = starArray[i].colorCenter + starArray[i].colorArea
        {{py setColorBounds(%min%,%max%, "%groupNames[i]%")}}
        $("#minColor").html((starArray[i].colorCenter - starArray[i].colorArea).toFixed(4));
        $("#maxColor").html((starArray[i].colorCenter + starArray[i].colorArea).toFixed(4));
        if (starArray[i].filterOn) {
            var min = starArray[i].filterCenter - starArray[i].filterArea
            var max = starArray[i].filterCenter + starArray[i].filterArea
            {{py setFilterBounds(%min%,%max%, "%currentVariableFilter[i]%", "%groupNames[i]%")}}
        } else {
            {{py setFilterBounds(0,100,0, "%groupNames[i]%")}}
        }
        //for (var j = starArray[i].variables.length - 1; j >= 0; j--) {
        //    if (currentFilterSettings[i][j] && starArray[i].filterOn ){
            //    {{py setFilterBounds(%currentFilterSettings[i][j].min%,%currentFilterSettings[i][j].max%, "%starArray[i].variables[j]%", "%groupNames[i]%")}}
        //    }
        //}
        if (starArray[i].isLog  ){
            {{py setLogColor(True,"%groupNames[i]%")}}
        } else {
            {{py setLogColor(False,"%groupNames[i]%")}}
        }
    }
    requestAnimationFrame(update);
}
update()

function updateTables() {
    for (var i = currentFilterSettings.length - 1; i >= 0; i--) {
        // console.log(currentVariableColor)
        var j = currentVariableColor[i]
        console.log(j)
        console.log(currentFilterSettings[i][j])
        if (currentColorSettings[i][j]){
            currentColorSettings[i][j].on = starArray[i].isLog
            console.log('saving new value:', currentColorSettings[i][j].on )
            currentColorSettings[i][j].min = starArray[i].colorRange[0]
            currentColorSettings[i][j].max = starArray[i].colorRange[1]
        }
        j = currentVariableFilter[i]
        if (currentFilterSettings[i][j]) {

            currentFilterSettings[i][j].on = starArray[i].filterOn
            console.log("saving value", currentFilterSettings[i][j].on)
            currentFilterSettings[i][j].min = starArray[i].filterRange[0]
            currentFilterSettings[i][j].max = starArray[i].filterRange[1]
        }
        if (starArray[i].isLog) {
            {{py setLogColor("True",%i%)}}
        } else {
            {{py setLogColor("False",%i%)}}
        }
    }
}