import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { AppComponent } from './app.component';
import { Collection } from './models/collection.model';
import { ApiService } from './services/api.service';

describe('AppComponent', () => {
  let fixture: ComponentFixture<AppComponent>;
  let app: AppComponent;
  let apiService: jasmine.SpyObj<ApiService>;

  beforeEach(async () => {
    localStorage.removeItem('edhremixer_current_profile');
    localStorage.removeItem('edhremixer_collections_profile_1');
    apiService = jasmine.createSpyObj<ApiService>('ApiService', [
      'getDeckName',
      'reshuffle',
    ]);
    apiService.getDeckName.and.returnValue(of({ name: 'Test collection' }));
    apiService.reshuffle.and.returnValue(of(new Blob()));

    await TestBed.configureTestingModule({
      imports: [AppComponent],
      providers: [{ provide: ApiService, useValue: apiService }],
    }).compileComponents();

    fixture = TestBed.createComponent(AppComponent);
    app = fixture.componentInstance;
  });

  it('creates the collection manager', () => {
    expect(app).toBeTruthy();
    expect(app.title).toBe('Collection Manager');
  });

  it('shows active source and target counts', () => {
    app.collections = [
      makeCollection('Source deck', true),
      makeCollection('Target deck', false),
      { ...makeCollection('Paused deck', true), active: false },
    ];

    fixture.detectChanges();

    const summary = fixture.nativeElement.querySelector(
      '.workflow-summary'
    ) as HTMLElement;
    expect(summary.textContent).toContain('Sources');
    expect(summary.textContent).toContain('Targets');
    expect(summary.textContent).toContain('1');
  });

  it('opens the review before submitting a reshuffle', () => {
    app.collections = [
      makeCollection('Source deck', true),
      makeCollection('Target deck', false),
    ];

    app.reshuffle();
    fixture.detectChanges();

    expect(app.showReshuffleReview).toBeTrue();
    expect(apiService.reshuffle).not.toHaveBeenCalled();
    expect(
      (fixture.nativeElement as HTMLElement).querySelector('[role="dialog"]')
    ).toBeTruthy();
  });

  it('requires at least one active source and target', () => {
    app.collections = [makeCollection('Source deck', true)];

    app.reshuffle();

    expect(app.showReshuffleReview).toBeFalse();
    expect(app.errorMessage).toBe(
      'At least one collection must be a target.'
    );
    expect(apiService.reshuffle).not.toHaveBeenCalled();
  });
});

function makeCollection(name: string, isSource: boolean): Collection {
  return {
    name,
    url: `https://www.moxfield.com/decks/${name}`,
    is_source: isSource,
    priority: 3,
    active: true,
    include_sideboard: false,
  };
}
