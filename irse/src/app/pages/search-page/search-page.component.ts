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
  constructor(private http: HttpClient) { }

  ngOnInit() {
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
    var advancedSet = this.checkAdvancedQuery()
    if ( (this.search_query === '' || this.search_query === null ) && !advancedSet) {
      this.error = true;
      this.loading = false;
    } else {
      this.error = false;
      this.loading = true;
      if(advancedSet){
        this.http.post(this.backend_server_location + '/search_faceted', {"facQuery" : this.advanced_query } ).subscribe(data => {
          console.log(data);
          this.loading = true
        })
      } else {
        this.http.post(this.backend_server_location + '/search_general', {"searchQuery" : this.search_query } ).subscribe(data => {
          console.log(data);
          this.loading = true
        })
      }
    }
  }

}
