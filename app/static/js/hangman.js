var GameBox = React.createClass({
    getInitialState: function () {
        return {data:{}};
    },

    handleGameSubmit: function(guess) {
        $.ajax({
            url: this.props.url,
            contentType: "application/json",
            datatype: 'json',
            type: 'PUT',
            data: JSON.stringify(guess),
            success: function(data) {
                this.setState({data:data});
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },

    handleNewGameClick: function(submit) {
        $.ajax({
            url: "http://localhost:5000/new_game", // hardcoded for now 
            contentType: "application/json",
            datatype: 'json',
            type: 'PUT',
            data: JSON.stringify(submit),
            success: function(data) {
                this.setState({data:data});
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },

    componentDidMount: function() {
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            success: function(data) {
                this.setState({data:data});
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },

    render: function() {
        // render form only when game state is "continue"
        var partial;
        if (this.state.data.result === "continue") {
            partial = <GameForm onGameSubmit={this.handleGameSubmit} data={this.state.data} />
        }
        return (
            <div className="gameBox">
                <h2>Hangman!</h2>
                <SessionStats data={this.state.data} />
                <GallowsGraphic data={this.state.data} />
                <WordFields data={this.state.data} />
                <GameMessage data={this.state.data} />
                {partial}
                <NewGameButton onNewGameClick={this.handleNewGameClick} data={this.state.data} />
            </div>
        );
    }
});

var GameForm = React.createClass({
    handleSubmit: function(e) {
        //gets field values
        e.preventDefault();
        var spot = this.refs.spot.getDOMNode().value.trim();
        var letter = this.refs.letter.getDOMNode().value.trim();
        var sessionID = this.props.data.sessionID
        if (!spot || !letter) {
            return;
        }
        this.props.onGameSubmit({spot: spot, letter: letter, sessionID: sessionID});
        //clear field values
        this.refs.spot.getDOMNode().value = '';
        this.refs.letter.getDOMNode().value = '';
        // move cursor back to spot
        this.refs.spot.getDOMNode().focus();
        return;
    },
    render: function() {
        return(
            <form className="gameForm" onSubmit={this.handleSubmit}>
                <h4>Guess</h4>
                <label for="spot">Spot (index starting at 0)</label>
                <input type="text" id="spot" ref="spot" />
                <label for="letter">Letter</label>
                <input type="text" id="letter" ref="letter" />
                <input type="submit" value="Submit" />
            </form>
        );
    }
});

var NewGameButton = React.createClass({
    handleClick: function(e) {
        e.preventDefault();
        var sessionID = this.props.data.sessionID
        this.props.onNewGameClick({sessionID: sessionID});
        return;
    },
    render: function() {
        return(
            <button className="newGameButton" onClick={this.handleClick}>
            New Game
            </button>
        );
    }
});

var GameMessage = React.createClass({
    render: function() {
        return(
            <div className="gameMessage">
                <p><em>Message: </em>{this.props.data.message}</p>
            </div>
        );
    }
});


var WordFields = React.createClass({
    render: function() {
        return(
            <div className="wordFields">
                <h3>Word</h3>
                The word is {this.props.data.current}
            </div>
        );
    }
});

var GallowsGraphic= React.createClass({
    render: function() {
        var gallow = "./media/h".concat(this.props.data.wrong, ".png");
        var divStyle = {
            borderStyle: 'solid',
            borderWidth: '2px'
        };
        return(
            <div className="gallowGraphic">
                <h3>The Gallows</h3>
                <img style={divStyle} src={gallow} alt="gallows" height="200" width="200" /> 
                <p>The # of wrong guesses is {this.props.data.wrong}</p>
            </div>
        );
    }
});

var SessionStats= React.createClass({
    render: function() {
        return(
            <div className="sessionStats">
                sessionID: {this.props.data.sessionID}
                <p><em>Session Stats: </em>wins = {this.props.data.sessionWins}, losses = {this.props.data.sessionLosses}</p>
            </div>
        );
    }
});

React.render(
    <GameBox url="http://localhost:5000/game_state" />,
    document.getElementById('content')
);
