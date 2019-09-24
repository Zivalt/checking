import {square_value, get_position} from './App'
import {is_defined_square_value} from './App'
import React from 'react';
import Square from './Square'

class Row extends React.Component{
    constructor(props){
        super(props);

    }
    render_square(i){
        return(
            <Square
                row = {this.props.id}
                column = {i}
                value = {get_position(is_defined_square_value(
                    this.props.values), i)}
                color = {square_value(is_defined_square_value(
                    this.props.values), i)}
                handle_render = {this.props.handle_render}/>
        );
    }
    render(){
        return(
            <div >
                {this.render_square(0)}
                {this.render_square(1)}
                {this.render_square(2)}
                {this.render_square(3)}
                {this.render_square(4)}
                {this.render_square(5)}
                {this.render_square(6)}
                {this.render_square(7)}
            </div>
      );
  }
}

export default Row;
