import { Component, OnInit } from '@angular/core';

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
  constructor() { }

  ngOnInit() {
  }

  startSearch(){
    if (this.search_query === '' || this.search_query === null) {
      this.error = true
    } else {
      this.error = false;
      this.loading = true;
    }
  }

}
