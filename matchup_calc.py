from random import uniform, choice

def getStrikeResults(stageRatios, counterStages):
  '''
  Takes in a dictionary of stage ratios and returns the most "balanced" stage.
  Intended to simulate the stage striking process.
  '''
  # filter out the counterpick stages
  strikeStageRatios = {key:value for (key,value) in stageRatios.items() if key not in counterStages}

  # half the time, second person strikes first
  if choice([True, False]):
    strikeStageRatios = {key:(1-value) for (key,value) in strikeStageRatios.items()}

  def strikeWorstStage(stages):
    worstStage = ['', 999]
    for k, v in stages.items():
      if v < worstStage[1]:
        worstStage = [k, v]
    strikeStageRatios.pop(worstStage[0])    

  # strike one stage
  strikeWorstStage(strikeStageRatios)
  
  # switch striker and strike two stages
  strikeStageRatios = {key:(1-value) for (key,value) in strikeStageRatios.items()}
  strikeWorstStage(strikeStageRatios)
  strikeWorstStage(strikeStageRatios)

  # switch striker and strike last stage
  strikeStageRatios = {key:(1-value) for (key,value) in strikeStageRatios.items()}
  strikeWorstStage(strikeStageRatios)

  # only one stage remaining -- return that
  return list(strikeStageRatios.keys())[0]

def simSet(stageRatios, counterStages, setLength, winnerBans, DSR=True):
  # for now assuming b05 and DSR
  currentStage = getStrikeResults(stageRatios, counterStages)
  stagesRemaining = stageRatios

  def simMatch(p1WinChance, winCounter):
    
    if uniform(0, 1.0) < p1WinChance:
      winCounter[0] += 1
      loser = 'p2'
    else:
      winCounter[1] += 1
      loser = 'p1'
    
    return loser, winCounter

  setCount = [0,0]
  p1_won_stages = []
  p2_won_stages = []

  while setCount[0] < (setLength/2 + 1/2) and setCount[1] < (setLength/2 + 1/2):
    # simulate the winner of the match and keep track of it
    loser, setCount = simMatch(stageRatios[currentStage], setCount)

    # switch stage based off who won
    if loser == 'p1':

      # remove the stage from the pool if DSR is on
      if DSR:
        p2_won_stages.append(currentStage)
      
      # if ban, then p2 strikes worst stage
      if winnerBans:
        reversedRatios = {key:(1-value) for (key,value) in stagesRemaining.items()}
        banned_stage = ''
        worstStage = ['', 999]
        for k, v in reversedRatios.items():
          if v < worstStage[1]:
            worstStage = [k, v]
            banned_stage = k

      # pick best stage remaining that's not DSR'd or banned
      bestStage = ['', 0]
      for k, v in stagesRemaining.items():
        if (v > bestStage[1]) and (k not in p1_won_stages) and (k != banned_stage):
          bestStage = [k, v]
          currentStage = k
  
    elif loser == 'p2':
      reversedRatios = {key:(1-value) for (key,value) in stagesRemaining.items()}

      # remove the stage from the pool if DSR is on
      if DSR:
        p1_won_stages.append(currentStage)

      # if ban, then p1 bans worst stage
      if winnerBans:
        banned_stage = ''
        worstStage = ['', 999]
        for k, v in stageRatios.items():
          if v < worstStage[1]:
            worstStage = [k, v]
            banned_stage = k
    
      # pick best stage remaining that's not DSR'd or banned
      bestStage = ['', 0]
      for k, v in reversedRatios.items():
        if (v > bestStage[1]) and (k not in p2_won_stages) and (k != banned_stage):
          bestStage = [k, v]
          currentStage = k

  if setCount[0] == 3:
    return 'p1'
  else:
    return 'p2'

def calculateMatchup(stageRatios, counterStages, setLength, loserBans, DSR=True):
  winCount = [0,0]
  
  for _ in range(100000):
    winner = simSet(stageRatios, counterStages, setLength, loserBans, DSR)
    if winner == 'p1':
      winCount[0] += 1
    elif winner == 'p2':
      winCount[1] += 1
  
  ratio = round(winCount[0] / (winCount[0]+winCount[1]) , 2)
  print('The matchup ratio is %i/%i P1:P2.' %  (ratio*100, round(1-ratio, 2)*100) )

stageRatios = {'BF': .5, 'YS': .5, 'DL': .5, 'FoD': .5, 'FD': .9, 'PS': .5}
counterStages = ['FD']
calculateMatchup(stageRatios, counterStages, setLength=5, loserBans=True, DSR=True)