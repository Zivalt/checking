import {is_defined, get_position} from './App'
import React from 'react';
import axios from 'axios';
class Square extends React.Component {
  constructor(props){
    super(props);
    const value = this.props.value

   }
  handle_click(){
    console.log(this.props.value)
    const parameter = {"data" : this.props.value}
    axios.post('http://localhost:5000/pick',parameter).then(
        response => {
            this.props.handle_render()
        })

  }

  render() {
    return (
        <button
            className="square"
            style = {{color: this.props.value.color,
            background: square_background(
                this.props.row,this.props.column)}}
            id = {this.props.id}
            onClick={() =>this.handle_click()}
           >
            {this.props.color}
        </button>
    );
  }

}


function square_background(row,column){
    if(is_defined(row) & is_defined(column)){
        if ((row+column)%2 === 0){
            return "white"
        }
        else{
            return "blue"
        }
    }
}

export default Square;
