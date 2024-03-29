import React, { Component } from 'react'
import { connect } from 'react-redux'
import { setCycle } from '../actions/gameActions'
import ScoreBoard from './score/ScoreBoard'
import ActionUser from './actions/ActionUser'
import Start from './cycle/Start'
import End from './cycle/End'
import * as GameSettings from '../utils/gameSettings'
import { END } from '../utils/constants'
import ActionComputer from './actions/ActionComputer'
import SetScore from './score/SetScore'
import LoginSignup from './loging/logingsignup'
import isLoggedIn from './loging/logingsignup'

class Main extends Component {

  /**
   * End game if user score or computer score reach max limit.
   * @param nextProps
   */
  componentWillUpdate(nextProps) {
    if (nextProps.userScore === GameSettings.VICTORY_SCORE || nextProps.computerScore === GameSettings.VICTORY_SCORE) {
      this.props.setCycle(END, true)
    }
  }

  render() {
    return (
      <div>
        {!this.props.gameStartedState ?
          <Start/>
          :
          <div>
            <ActionComputer/>
            <SetScore/>
            <ScoreBoard/>
            {this.props.gameEndedState ?
              <End/>
              :
              <ActionUser/>
            }
          </div>
        }
        </div>
      
    )
  }
}

const mapStateToProps = state => {
  return {
    gameStartedState: state.gameStartedState,
    gameEndedState: state.gameEndedState,
    userScore: state.userScore,
    computerScore: state.computerScore
  }
}

const mapDispatchToProps = { setCycle }

export default connect(mapStateToProps, mapDispatchToProps)(Main)
