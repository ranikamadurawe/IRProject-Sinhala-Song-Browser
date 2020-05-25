import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MusiclyricsPageComponent } from './musiclyrics-page.component';

describe('MusiclyricsPageComponent', () => {
  let component: MusiclyricsPageComponent;
  let fixture: ComponentFixture<MusiclyricsPageComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MusiclyricsPageComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MusiclyricsPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
