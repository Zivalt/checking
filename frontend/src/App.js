import React,{useState,useEffect} from 'react';
import axios from 'axios'
import './App.css';

class Square extends React.Component {
  constructor(props){
    super(props);
    const state = {}
    const value = this.props.value
   }
  handle_click(){
    console.log(this.props.value)
    const parameter = {"data" : this.props.value}
    axios.post('http://localhost:5000/pick',parameter).then(function (response) {
    console.log(response);
  })

  }

  render() {

    return (
      <button
        className="square"
        style = {{color: this.props.value.color,background: square_background(this.props.row,this.props.column)}}
        id = {this.props.id}
        onClick={() =>this.handle_click()}>
        {this.props.p}
      </button>
    );
  }
}


class Row extends React.Component{
    constructor(props){
        super(props);

    }
    render_square(i){
        return(
            <Square row = {this.props.id} column = {i} value = {is_defined_square_value(this.props.values[i])} p = {square_value(this.props.values[i])} />
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
class Board extends React.Component {
  constructor(props){
    super(props);

  }
  render_row(i){
    return(
        <div>
            <Row id = {i} values = {is_defined_row_value(this.props.values,"row".concat(i))} />
        </div>
    );

  }
  render(){
      return (
        <div>
            {this.render_row(0)}
            {this.render_row(1)}
            {this.render_row(2)}
            {this.render_row(3)}
            {this.render_row(4)}
            {this.render_row(5)}
            {this.render_row(6)}
            {this.render_row(7)}
        </div>
      );
  }


}
export default () => {
    const [board, setBoard] = useState({})
    const [turn, setTurn] = useState("")


     useEffect(() => {
         try{
            const fetch_data = async () => {
                 await axios.get('http://localhost:5000/').then(response => {
                    const data = response.data

                    setTurn(data.turn)
                    setBoard(data.board)
                 })
             }

            fetch_data()
        }catch(error){

        }

     })

      return (
        <div>
            <Board values = {board} />
            <h1>turn of {turn}</h1>
        </div>

      )


}

function is_defined_row_value(number,index= "row0"){
    if (is_defined(number[index])){
        return number[index]
    }
    else{
        return ""
    }
}
function is_defined_square_value(number){
    if(is_defined(number)){
        return number
    }
    else{
     return ""
    }
}

function is_defined(obj){
    if (typeof obj !== "undefined"){
        return true

    }
    else{
        return false
    }
}
function check_color(object,color){
    if(object === color){
        return true
    }
    return false
}
function square_value(obj){
    if(is_defined(obj)){
        const color = obj["color"]
        if (check_color(color,"red") || check_color(color,"black")){
            if (obj["is_king"] === true){
                return "X"
            }
            else{
                return "O"
            }
        }
        else{
            if (check_color(color,"*")){
                return "*"
            }
            else{
                return ""
            }
        }
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


