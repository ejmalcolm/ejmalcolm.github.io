function reverseRatios(ratios) {
    const newRatios = {};
    for (var key in ratios) {
        newRatios[key] = ratios[key]
    };
    return newRatios
}


function getStrikeResults(stageRatios, counterStages) {

    let strikeStageRatios = {};
    
    // filter out the counterpick stages
    for (var key in stageRatios) {
        if (Array.from(counterStages).indexOf(key) != 0) { 
            strikeStageRatios[key] = stageRatios[key]
        };
    };
    
    // half the time, second person strikes first
    if (Math.random() > 0.5) { 
        strikeStageRatios = reverseRatios(strikeStageRatios)
    };

    function strikeWorstStage(stages) {
        worstStage = ['', 999];
        for (var key in stages) {
            if (stages[key] < worstStage[1]) {
                worstStage = [k, stages[key]];
                delete strikeStageRatios[worstStage[0]];
            };
        };
    };

    //strikeWorstStage(strikeStageRatios)
    console.log(strikeStageRatios)

}

let stageRatios = {'BF': .5, 'YS': .5, 'DL': .5, 'FoD': .5, 'FD': .9, 'PS': .5};
let counterStages = ['FD']

getStrikeResults(stageRatios, counterStages)