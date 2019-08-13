import React,{useState,useEffect} from 'react';
import axios from 'axios'
import './App.css';

class Square extends React.Component {
  constructor(props){
    super(props);
    const state = {board : null}
    const value = this.props.value

   }
  handle_click(){
    const parameter = {"data" : this.props.value}
    axios.post('http://localhost:5000/pick',parameter).then(response => {
    console.log(this)
    this.props.handle_render()
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
            <Square row = {this.props.id} column = {i} value = {is_defined_square_value(this.props.values[i])} p = {square_value(this.props.values[i])}
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
class Board extends React.Component {
  constructor(props){
    super(props);

  }
  render_row(i){
    return(
        <div>
            <Row id = {i} handle_render = {this.props.handle_render} values = {is_defined_row_value(this.props.values,"row".concat(i))} />
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
class App extends React.Component{
constructor(props){
    super(props)
    this.handle_render = this.handle_render.bind(this)}
    state = {turn: "",board: null,count: 0}

     handle_render(){
        this.change_data()
     }
     change_data(){
          try{
             const fetch_data = async () => {
                  await axios.get('http://localhost:5000/').then(response => {
                     const data = response.data
                     this.setState({turn:data.turn, board:data.board})
                  })
              }

             fetch_data()
         }catch(error){

         }
         }
     componentWillMount(){
        this.change_data()

     }

    render(){
      return (
        <div>
            <Board values = {not_null(this.state.board)} handle_render = {this.handle_render} />
            <h1>turn of {not_null(this.state.turn)}</h1>
        </div>

      )}


}

function is_defined_row_value(number,index= "row0"){
    if (is_defined(number[index])){
        return number[index]
    }
    else{
        return ""
    }
}
function not_null(obj){
    if(obj !== null){
        return obj
    }else{ return false
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

export default App;
