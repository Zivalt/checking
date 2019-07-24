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
    const paramator = {"data" : this.props.value}
    axios.post('http://localhost:5000/pick',paramator).then(function (response) {
    console.log(response);
  })

  }

  render() {

    return (
      <button
        className="square"
        id = {this.props.id}
        onClick={() =>this.handle_click()}>
        {this.props.value.color}
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
            <Square key = {i} value = {is_defined_square_value(this.props.values[i])} />
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


