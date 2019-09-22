import React,{useState,useEffect} from 'react';
import axios from 'axios'
import './App.css';
import Board from './Board'

class App extends React.Component{
constructor(props){
    super(props)
    this.handle_render = this.handle_render.bind(this)
    this.state = {turn: "",board: null,count: 0}
    }

     handle_render(){
        this.fetch_board_data()
     }
     create_new_board(){
        fetch('http://localhost:5000/restart')
        this.fetch_board_data()
     }
     fetch_board_data(){
          try{
             const fetch_data = async () => {
                  await axios.get('http://localhost:5000/').then(response => {
                     const data = response.data
                     this.setState({turn:data.turn, board:data.board})
                     console.log(this.state)
                  })
              }

             fetch_data()
         }catch(error){

         }
         }
     componentWillMount(){
        this.fetch_board_data()

     }

    render(){
      return (
        <div>
            <Board
                values = {check_if_null(this.state.board)}
                handle_render = {this.handle_render}
             />
            <h1>turn of {this.state.turn}</h1>
            <button onClick = {() => this.create_new_board()}>start new game</button>

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


function check_if_null(obj){
    if(obj !== null){
        return obj
    }
    else
        {
         return false
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


function square_value(obj, y){
    var piece = get_position(obj,y)
    if(piece != ""){
        var color = piece["color"]
        if (check_color(color,"red") || check_color(color,"black")){
            if (piece["is_king"] === true){
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
        }
    }
    return ""
}


function get_position(obj, y){
    if (obj !== ""){
        for(var i = 0;i <= 3; i++){
            if (is_defined(obj[i])){
                var s2 = obj[i]["position"][1]
                if(s2 === y){
                    return obj[i]
                }
            }
        }
    }
    return ""
}

export default App;
export {square_value,check_color,is_defined,is_defined_square_value,check_if_null,is_defined_row_value, get_position};




