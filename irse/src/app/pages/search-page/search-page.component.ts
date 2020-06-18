import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-search-page',
  templateUrl: './search-page.component.html',
  styleUrls: ['./search-page.component.css']
})
export class SearchPageComponent implements OnInit {

  number_of_results : number = 0;
  search_query : string = '';
  loading = false;
  error = false;
  shown_results = [];
  results = [];
  aggregations = {
    "Artist Filter" : [],
    "Writer Filter" : [],
    "Composer Filter" : [],
    "Genre Filter":[],
    "Movie Filter":[],
    "View Filter":[]
  };
  backend_server_location = "http://localhost:5000"

  advanced_query = {
    "artist" : "",
    "writer": "",
    "composer":"",
    "genre":"",
    "movie":"",
    "key":"",
    "beat":"",
    "lyrics":"",
    "title":""
  }

  filter = {
    "artist" : "",
    "writer": "",
    "composer":"",
    "genre":"",
    "movie":"",
    "views":""
  }

  constructor(private http: HttpClient) { }

  ngOnInit() {
  }

  reset_filter() {
    this.filter = {
      "artist" : "",
      "writer": "",
      "composer":"",
      "genre":"",
      "movie":"",
      "views":""
    }
    this.shown_results = this.results
  }

  filter_query() {
    this.shown_results= this.results.filter(result => {
      var return_val = true;
      for (var key in this.filter) {
        if (key == "views"){
          var from = this.filter[key].split("-")[0]
          var to = this.filter[key].split("-")[1]
          if (from != "*"){
	    if (result['_source'][key] < parseInt(from)){
	       return_val = return_val && false;
	    } else {
               return_val = return_val && true;
            } 
          } else {
             return_val = return_val && true;
          }
          if (to != "*"){
            if (result['_source'][key] > parseInt(to)){
	       return_val = return_val && false;
	    } else {
               return_val = return_val && true;
            }
          } else {
             return_val = return_val && true;
          }
        } else {
          if (this.filter[key] == "" || this.filter[key] == null){
            return_val = return_val && true;
          } else {
            if(this.filter[key] == result['_source'][key]){
              return_val = return_val && true;
            } else {
              return_val = return_val && false;
            }
          }
        }
      }
      return return_val;
    });
  }

  checkAdvancedQuery(){
    var advancedOptionsSet = false;
    for (var key in this.advanced_query){
      if( !(this.advanced_query[key] == '') && !(this.advanced_query[key]== null) ){
        advancedOptionsSet = true;
        break;
      }
    }
    return advancedOptionsSet;
  }

  startSearch(){
    this.filter = {
      "artist" : "",
      "writer": "",
      "composer":"",
      "genre":"",
      "movie":"",
      "views":""
    }
    this.results = []
    this.shown_results = []
    var advancedSet = this.checkAdvancedQuery()
    if ( (this.search_query === '' || this.search_query === null ) && !advancedSet) {
      this.error = true;
      this.loading = false;
    } else {
      this.error = false;
      this.loading = true;
      if(advancedSet){
        this.http.post(this.backend_server_location + '/search_faceted', {"facQuery" : this.advanced_query } ).subscribe( (data: any[]) => {
          console.log(data)
          this.loading = false
          this.number_of_results = data.length;
          this.shown_results = data['hits']['hits'];
          this.aggregations = data['aggregrations']
          console.log(this.shown_results)
        })
      } else {
        this.http.post(this.backend_server_location + '/search_general', {"searchQuery" : this.search_query } ).subscribe( (data: any[]) => {
          console.log(data)
          this.loading = false
          this.number_of_results = data.length;
          this.shown_results = data['hits']['hits'];
          this.results = data['hits']['hits'];
          this.aggregations = data['aggregations']
          console.log(this.shown_results)
        })
      }
    }
  }

}
