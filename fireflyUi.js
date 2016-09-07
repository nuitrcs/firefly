// Create the UI
$( function() {
    $( "#console" ).dialog({
        // autoOpen: false,
        height: 90,
        resizable: false,
        width: 320,
        position: 'asdf',
        // right: 200px, /* use a length or percentage */ consoleDisplayed
        close: function(event,ui) {
            consoleDisplayed = false
        },
        open: function(event,ui) {
            consoleDisplayed = true
            //$(".ui-dialog-titlebar", ui.dialog | ui).hide();
            $('#console').dialog({ dialogClass: 'noTitleStuff' });
        }
    });
    $( "#helpBox" ).dialog({
        // position: [200, 200],
        // autoOpen: false,
        height: 400,
        width: 460,
        close: function(event,ui) {
            helpDisplayed = false
        },
        open: function(event,ui) {
            helpDisplayed = true
        }
    });
    $( "#colormapPreview" ).dialog({
        // position: [200, 200],
        // autoOpen: false,
        height: 'auto',
        width: 'auto',
        close: function(event,ui) {
            colormapDisplayed =  false
        },
        open: function(event,ui) {
            colormapDisplayed =  true
        }

    });
} );

var viewPanel
var starArray = new Array()
var controlKit
var helpDisplayed = false
var colormapDisplayed =  false
var consoleDisplayed = false
var screenDisplayed = false

////////////////////////////////////////////////////////////////////////////////
porthole.connected = function() {
    {{py print "started porthole connected function"}}
    controlKit = new ControlKit();
    //viewPanel = controlKit.addPanel({label: 'Star Group Settings' , fixed: false, width: 320,position: [5, 5]});
    //console.log(controlKit)
    //viewPanel = controlKit._panels[0]
    //console.log(viewPanel)
    $('#helpBox').dialog('close');
    $('#colormapPreview').dialog('close');
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

////////////////////////////////////////////////////////////////////////////////
function setColorMapArrays( cm, cml,cp) {
    colorMapArray = cm
    colorMapLabels = cml
    colorMapPaths = cp
}

////////////////////////////////////////////////////////////////////////////////
function setVariables( variables, ranges) {
    console.log("Variables Set")
    variableArray = variables
    variableRanges = ranges
}

////////////////////////////////////////////////////////////////////////////////
function printConsole(text) {
    text = "Another line of Text"
    consoleString = consoleString + "<BR>" + text
    $("#consoleText").html(consoleString)
    $('#console').animate({
        scrollTop: $('#console').scrollTop() + $('#console').height()
    });
}

////////////////////////////////////////////////////////////////////////////////
function setConsole(text) {
    $("#consoleText").html(text)
}

////////////////////////////////////////////////////////////////////////////////
function clearConsole(text) {
    consoleString = ""
    $("#consoleText").html(consoleString)
}

////////////////////////////////////////////////////////////////////////////////
function toggleHelp() {
    if (helpDisplayed) {
        $('#helpBox').dialog('close');
    } else {
        $('#helpBox').dialog('open');
    }
}

////////////////////////////////////////////////////////////////////////////////
function toggleConsole() {
    if (consoleDisplayed) {
        $('#console').dialog('close');
    } else {
        $('#console').dialog('open');
    }
}

////////////////////////////////////////////////////////////////////////////////
function  toggleColorMap() {
    if (colormapDisplayed) {
        $('#colormapPreview').dialog('close');
    } else {
        $('#colormapPreview').dialog('open');
    }
}

////////////////////////////////////////////////////////////////////////////////
controlData = {
    dataMode: null,
    selectedDataMode: null,
    useSmoothingLength: false,
    useLog: false,
    pointScale: 0.05,
    pointScaleRange: [0.001, 0.05],
    colormap: null,
    enableColormapper: false,
    colormapPaths: null,
    colormapMin: '0',
    colormapMax: '1',
    navspeed: 50,
    navspeedRange: [1, 100],
    filterMin: '0',
    filterMax: '1',
    camPosX: '0',
    camPosY: '0',
    camPosZ: '0',
    corPosX: '0',
    corPosY: '0',
    corPosZ: '0',
    decValue: 10,
    decValueRange: [1,100],
    useProg: true
};

////////////////////////////////////////////////////////////////////////////////
presetData = {
    presetList: ['noViewsSaved'],
    currentName: '',
    currentPresetIndex: 0
}
var currentPresetIndex = -1

function initializePresetPanels() {
    {{py print "======------Initializing Preset Panel------======"}}
    console.log("Preset Panel initialized")
    presetPanel = controlKit.addPanel({
        label: 'Presets',
        fixed: false, 
        width: 320,
        currentPresetIndex: -1,
        // align: 'left'//,
        position: [window.innerwidth - 320, 250]
    })
    if (presetData.presetList[0] == "noViewsSaved") {
        {{py print "no views saved"}}
        currentPresetIndex = -1
    } else {
        {{py print "previous files found"}}
        currentPresetIndex = 0
    }
    select = presetPanel.addSelect(presetData,'presetList' , {
            label: 'Preset', 
            onChange: function (index) {
                currentPresetIndex = index
                console.log(currentPresetIndex)
                {{py print "Applying Entry" , %currentPresetIndex%}}
            },
            target: 'currentPresetIndex'
        })
    presetPanel.addButton('Apply',function() {
            console.log("Applying Entry: ", currentPresetIndex)
            {{py print "Applying Entry" , %currentPresetIndex%}}
            if (currentPresetIndex != -1) {
                {{py setPresetView(%currentPresetIndex%)}} 
            }
        }, {})
    presetPanel.addStringInput(presetData,'currentName', { 
            label: 'Name'
        })
    presetPanel.addButton('Save Settings',function() { 
            console.log("Saving Entry: ", presetData.currentName)
            exportArray = []
            //exportArray = [1,2,3,4]
            presetData.presetList = presetData.presetList.concat([presetData.currentName])
            currentPresetIndex = presetData.presetList.length - 1
            presetData.currentPresetIndex = presetData.currentName
            {{py saveCurrentView("%presetData.currentName%")}}
            console.log("Adding new entry and Refreshing")
            console.log(presetData.presetList)
            controlKit.update();
        }, {})
    presetPanel.addButton('Delete Current Entry',function() {
            console.log("Deleting Entry: ", currentPresetIndex)
            if (currentPresetIndex != -1) {
                {{py eraseView(%currentPresetIndex%)}} 
                presetData.presetList.splice(currentPresetIndex,1)
                presetData.currentPresetIndex = presetData.currentPresetIndex - 1
                controlKit.update()
            }
        }, {})
}

function settingPresets( nameList ){
    // {{py print "setting presets : " , "%nameList%"}}
    presetData.presetList = nameList
}

var controls
////////////////////////////////////////////////////////////////////////////////
function initializeControls(modes, colormaps, colormapFiles, filterModes, kernelModes, renderModes) {
    {{py print "======------Initializing Control Panel------======"}}

    controlData.dataMode = modes;
    controlData.selectedDataMode = modes[0];
    controlData.colormap = colormaps;
    controlData.selectedColormap = colormaps[0];
    controlData.colormapPaths = colormapFiles;
    // controlData.colormapPaths = colormapFiles;

    controlData.filterMode = filterModes;
    controlData.selectedFilterMode = filterModes[0];
    controlData.kernelMode = kernelModes;
    // controlData.kernelModeInd = 0
    controlData.selectedKernelMode = kernelModes[0];
    controlData.renderMode = renderModes;
    controlData.selectedRenderMode = renderModes[0];
    // controlData.renderModeInd = 0

    
    controls = controlKit.addPanel({
        label: 'Options', 
        fixed: false, 
        width: 400,
        position: [window.innerWidth - 400, 50]
    });
    
    // Data panel
    controls.addGroup({label: 'Data', enable: false})
        .addSelect(controlData, 'dataMode' , {
            label: 'Display', 
            onChange: function (index) {
                controlData.selectedDataMode = controlData.dataMode[index];
                {{py setDataMode(%index%)}}
                $("#cColorvariable").html(controlData.selectedDataMode)
            },
            target: 'selectedDataMode'
        })
        .addCheckbox(controlData, 'useSmoothingLength', {
            label: 'Smoothing Length Enabled',
            onChange: function () {
                {{py enableSmoothingLength(%controlData.useSmoothingLength%)}}
            }
        })
        .addCheckbox(controlData, 'useLog', {
            label: 'Log Scale',
            onChange: function () {
                {{py enableLogScale(%controlData.useLog%)}}
            }
        })
        .addSlider(controlData, 'pointScale','pointScaleRange', {
            label : 'Point Scale:', 
            dp: 3,
            onFinish: function() {
                {{py setPointScale(%controlData.pointScale%)}}
            }
        })
        .addSelect(controlData, 'kernelMode' , {
            label: 'Kernel', 
            onChange: function (index) {
                controlData.selectedKernelMode = controlData.kernelMode[index];
                {{py setKernelMode(%index%)}}
            },
            target: 'selectedKernelMode'
        })
        .addSelect(controlData, 'renderMode' , {
            label: 'Draw Mode', 
            onChange: function (index) {
                controlData.selectedRenderMode = controlData.renderMode[index];
                {{py setRenderMode(%index%)}}
            },
            target: 'selectedRenderMode'
        })
        .addCheckbox(controlData, 'enableColormapper', {
            label: 'Advanced Colormapper',
            onChange: function () {
                {{py enableColormapper(%controlData.enableColormapper%)}}
            }
        })
        .addSelect(controlData, 'colormap' , {
            label: 'Color Map', 
            onChange: function (index) {
                controlData.selectedColormap = controlData.colormap[index];

                $("#colorMapImg").attr('src',controlData.colormapPaths[index]);
                {{py setColormap(%index%)}}
                // updateTables()
            },
            target: 'selectedColormap'
        })
        .addStringInput(controlData,'colormapMin', { 
            label: 'Colormap Min'
        })
        .addStringInput(controlData,'colormapMax', { 
            label: 'Colormap Max'
        })
        .addButton('Update Bounds',function() { 
                $('#minColor').html(controlData.colormapMin)
                $('#maxColor').html(controlData.colormapMax)
                {{py updateColormapBounds(%controlData.colormapMin%, %controlData.colormapMax%) }}
            }, {}
        )
        .addButton('Reset Bounds',function() { 
                {{py resetColormapBounds() }}
            }, {}
        )
    
    // Filter panel
    filterPanel = controls.addGroup({label: 'Filter', enable: false})
        .addSelect(controlData, 'filterMode' , {
            label: 'Filter Mode', 
            onChange: function (index) {
                controlData.selectedFilterMode = controlData.filterMode[index];
                {{py setFilterMode(%index%)}}
            }
        })
        .addStringInput(controlData,'filterMin', { 
            label: 'Min'
        })
        .addStringInput(controlData,'filterMax', { 
            label: 'Max'
        })
        .addButton('Update Filter',function() { 
                {{py updateFilterBounds(%controlData.filterMin%, %controlData.filterMax%) }}
            }, {}
        )
        .addButton('Reset Filter',function() { 
                {{py resetFilterBounds() }}
            }, {}
        )
   
    // View panel
    controls.addGroup({label: 'View', enable: false})
        .addSlider(controlData, 'navspeed','navspeedRange', {
            label : 'Navigation Speed:', 
            dp: 0,
            onFinish: function() {
                {{py panSpeed = %controlData.navspeed%}}
            }
        })
        .addSlider(controlData, 'decValue','decValueRange', {
            label : 'Decimation Value:', 
            dp: 0,
            onFinish: function() {
                {{py setDecimationValue(%controlData.decValue%)}}
            }
        })
        .addCheckbox(controlData, 'useProg', {
            label: 'Enable Progressive',
            onChange: function () {
                {{py enableProgressive(%controlData.useProg%)}}
            }
        })
        .addButton('Save Image',function() { {{py saveViewImage() }} }, {}
        )
        .addSubGroup({label: 'Camera Position', enable: false})
            .addStringInput(controlData,'camPosX', { 
                label: 'X-Pos:'
            })
            .addStringInput(controlData,'camPosY', { 
                label: 'Y-Pos:'
            })
            .addStringInput(controlData,'camPosZ', { 
                label: 'Z-Pos:'
            })
            .addButton('Update Position', function() {
                {{py requestUpdatePos()}}
            }, {})
            .addButton('Apply',function() { 
                    console.log("Applying camera Pos")
                    {{py setCamPos('%controlData.camPosX%','%controlData.camPosY%','%controlData.camPosZ%')}}
                    //{{py camera.setPosition(Vector3(%controlData.camX%,%controlData.camY%,%controlData.camZ%))}}
                }, {})
        .addSubGroup({label: 'Center of Rotation', enable: false})
            .addStringInput(controlData,'corPosX', { 
                label: 'X-Pos:'
            })
            .addStringInput(controlData,'corPosY', { 
                label: 'Y-Pos:'
            })
            .addStringInput(controlData,'corPosZ', { 
                label: 'Z-Pos:'
            })
            .addButton('Apply',function() { 
                    console.log("Applying center of Rotation Pos")
                    {{py setPivotPoint('%controlData.corPosX%','%controlData.corPosY%','%controlData.corPosZ%')}}
                }, {})
            .addButton('Center on Rotation Point',function() { 
                    console.log("Applying center of Rotation Pos")
                    {{py lookAtPivot()}}
                }, {})
    {{py updatePythonInterface()}}
}  

////////////////////////////////////////////////////////////////////////////////
function updateColormapBounds(cmin, cmax) {
    controlData.colormapMin = cmin;
    controlData.colormapMax = cmax;
    console.log("Updating colormap bounds")
    controlKit.update();
}

////////////////////////////////////////////////////////////////////////////////
function updateCameraPos(x,y,z) {
    // console.log(controls)
    // console.log(controls._groups[2]._subGroups[1]._enabled)
    // if (controls._groups[2]._subGroups[1]._enabled == false) {
    console.log("Cam pos updated")
    controlData.camPosX = x
    controlData.camPosY = y
    controlData.camPosZ = z
    controlKit.update()
}

////////////////////////////////////////////////////////////////////////////////
function updateCenterOfRotation(x,y,z) {
    controlData.corPosX = x
    controlData.corPosY = y
    controlData.corPosZ = z
    controlKit.update()
}

function postLoadUpdate(sDMode, uSL,uL,pS,eCM,sCM, cmMin,cmMax, x,y,z,corX,corY,corZ, rM, kM,progScan,dC) {
    console.log("datmode: " , sDMode)
    controlData.selectedDataMode = controlData.dataMode[sDMode]
    console.log(uSL)
    controlData.useSmoothingLength = uSL
    console.log(uL)
    controlData.useLog = uL
    console.log(pS)
    controlData.pointScale = pS
    console.log(eCM)
    controlData.enableColormapper = eCM
    console.log("colormap: ", sCM)
    controlData.selectedColormap = controlData.colormap[sCM]
    console.log(cmMin,cmMax)
    controlData.colormapMin = cmMin
    controlData.colormapMax = cmMax
    controlData.camPosX = x 
    controlData.camPosY = y 
    controlData.camPosZ = z
    controlData.corPosX = corX
    controlData.corPosY = corY 
    controlData.corPosZ = corZ
    console.log("rnder: ", rM)
    controlData.selectedRenderMode = controlData.renderMode[ rM ]
    console.log("kernelMode ", kM)
    controlData.selectedKernelMode = controlData.kernelMode[ kM ]
    controlData.progScan = progScan
    control.decValue = dC
    $("#cColorvariable").html(controlData.selectedDataMode)
    $('#minColor').html(controlData.colormapMin)
    $('#maxColor').html(controlData.colormapMax)

    controlKit.update();
}



