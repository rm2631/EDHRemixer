import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { Collection } from './models/collection.model';
import { ApiService } from './services/api.service';

type SortColumn = 'name' | 'url' | 'type';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent {
  title = 'Collection Manager';
  collections: Collection[] = [];
  url: string = '';
  loading: boolean = false;
  loadingMessage: string = '';
  showReshuffleReview: boolean = false;
  errorMessage: string = '';
  successMessage: string = '';
  sortColumn: SortColumn | null = null;
  sortAscending: boolean = true;

  // Profile management
  currentProfile: number = 1;
  profiles: number[] = [1, 2, 3];
  private readonly STORAGE_KEY_PREFIX = 'edhremixer_collections_profile_';
  private readonly CURRENT_PROFILE_KEY = 'edhremixer_current_profile';

  constructor(private apiService: ApiService) {
    this.loadCurrentProfile();
    this.loadCollections();
  }

  private loadCurrentProfile(): void {
    try {
      const stored = localStorage.getItem(this.CURRENT_PROFILE_KEY);
      if (stored) {
        const profile = parseInt(stored, 10);
        if (this.profiles.includes(profile)) {
          this.currentProfile = profile;
        }
      }
    } catch (error) {
      console.error('Error loading current profile:', error);
    }
  }

  private saveCurrentProfile(): void {
    try {
      localStorage.setItem(
        this.CURRENT_PROFILE_KEY,
        this.currentProfile.toString()
      );
    } catch (error) {
      console.error('Error saving current profile:', error);
    }
  }

  switchProfile(profileNumber: number): void {
    if (this.currentProfile === profileNumber) {
      return;
    }
    this.currentProfile = profileNumber;
    this.saveCurrentProfile();
    this.loadCollections();
    this.successMessage = `Switched to Profile ${profileNumber}`;
    this.clearMessages();
  }

  getProfileStorageKey(): string {
    return `${this.STORAGE_KEY_PREFIX}${this.currentProfile}`;
  }

  get activeSourceCollections(): Collection[] {
    return this.collections.filter(
      (collection) => collection.active && collection.is_source
    );
  }

  get activeTargetCollections(): Collection[] {
    return this.collections.filter(
      (collection) => collection.active && !collection.is_source
    );
  }

  get activeCollectionCount(): number {
    return this.collections.filter((collection) => collection.active).length;
  }

  get inactiveCollectionCount(): number {
    return this.collections.filter((collection) => !collection.active).length;
  }

  private loadCollections(): void {
    try {
      const stored = localStorage.getItem(this.getProfileStorageKey());
      if (stored) {
        this.collections = JSON.parse(stored);
        // Migrate existing collections to have priority, active, and include_sideboard fields if missing
        this.collections = this.collections.map((c) => ({
          ...c,
          priority: c.priority !== undefined ? Number(c.priority) : 3,
          active: c.active !== undefined ? c.active : true,
          include_sideboard:
            c.include_sideboard !== undefined ? c.include_sideboard : false,
        }));
        this.saveCollections();
      } else {
        // No data for this profile - clear collections
        this.collections = [];
      }
    } catch (error) {
      console.error('Error loading collections from localStorage:', error);
      this.collections = [];
    }
  }

  private saveCollections(): void {
    try {
      localStorage.setItem(
        this.getProfileStorageKey(),
        JSON.stringify(this.collections)
      );
    } catch (error) {
      console.error('Error saving collections to localStorage:', error);
    }
  }

  addCollection(): void {
    this.errorMessage = '';
    this.successMessage = '';
    this.showReshuffleReview = false;

    if (!this.url.trim()) {
      this.errorMessage = 'URL cannot be empty.';
      return;
    }

    if (!this.url.toLowerCase().includes('moxfield')) {
      this.errorMessage = 'URL must be a valid Moxfield URL.';
      return;
    }

    this.loading = true;
    this.loadingMessage = 'Looking up collection…';
    this.apiService.getDeckName(this.url).subscribe({
      next: (response) => {
        const newCollection: Collection = {
          name: response.name,
          url: this.url,
          is_source: true,
          priority: 3,
          active: true,
          include_sideboard: false,
        };
        this.collections.push(newCollection);
        this.saveCollections();
        this.url = '';
        this.successMessage = 'Collection added successfully!';
        this.loading = false;
        this.loadingMessage = '';
        this.clearMessages();
      },
      error: (error) => {
        this.errorMessage = `Error fetching deck name: ${
          error.error?.error || error.message
        }`;
        this.loading = false;
        this.loadingMessage = '';
        this.clearMessages();
      },
    });
  }

  deleteCollection(index: number): void {
    const collection = this.sortedCollections()[index];
    const originalIndex = this.collections.indexOf(collection);
    this.collections.splice(originalIndex, 1);
    this.saveCollections();
    this.successMessage = `Deleted ${collection.name}`;
    this.clearMessages();
  }

  toggleType(index: number): void {
    const collection = this.sortedCollections()[index];
    const originalIndex = this.collections.indexOf(collection);
    collection.is_source = !collection.is_source;
    this.collections[originalIndex].is_source = collection.is_source;
    this.saveCollections();
  }

  toggleActive(index: number): void {
    const collection = this.sortedCollections()[index];
    const originalIndex = this.collections.indexOf(collection);
    collection.active = !collection.active;
    this.collections[originalIndex].active = collection.active;
    this.saveCollections();
  }

  toggleSideboard(index: number): void {
    const collection = this.sortedCollections()[index];
    const originalIndex = this.collections.indexOf(collection);
    collection.include_sideboard = !collection.include_sideboard;
    this.collections[originalIndex].include_sideboard =
      collection.include_sideboard;
    this.saveCollections();
  }

  updatePriority(index: number): void {
    const collection = this.sortedCollections()[index];
    const originalIndex = this.collections.indexOf(collection);
    this.collections[originalIndex].priority = collection.priority;
    this.saveCollections();
  }

  reshuffle(): void {
    this.errorMessage = '';
    this.successMessage = '';
    this.showReshuffleReview = false;

    if (this.activeCollectionCount === 0) {
      this.errorMessage =
        'No active collections to process. Activate a collection first.';
      this.clearMessages();
      return;
    }

    if (this.activeSourceCollections.length === 0) {
      this.errorMessage = 'At least one collection must be a source.';
      this.clearMessages();
      return;
    }

    if (this.activeTargetCollections.length === 0) {
      this.errorMessage = 'At least one collection must be a target.';
      this.clearMessages();
      return;
    }

    this.showReshuffleReview = true;
  }

  confirmReshuffle(): void {
    this.showReshuffleReview = false;
    this.loading = true;
    this.loadingMessage = 'Reshuffling collections…';
    this.apiService.reshuffle(this.collections).subscribe({
      next: (blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'reshuffled.xlsx';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        this.successMessage = 'Engine ran successfully! File downloaded.';
        this.loading = false;
        this.loadingMessage = '';
        this.clearMessages();
      },
      error: (error) => {
        this.errorMessage = `Error running the engine: ${
          error.error?.error || error.message
        }`;
        this.loading = false;
        this.loadingMessage = '';
        this.clearMessages();
      },
    });
  }

  sortBy(column: SortColumn): void {
    if (this.sortColumn === column) {
      this.sortAscending = !this.sortAscending;
    } else {
      this.sortColumn = column;
      this.sortAscending = true;
    }
  }

  sortedCollections(): Collection[] {
    if (!this.sortColumn) {
      return this.collections;
    }

    const sorted = [...this.collections];
    sorted.sort((a, b) => {
      let compareValue = 0;

      switch (this.sortColumn) {
        case 'name':
          compareValue = a.name
            .toLowerCase()
            .localeCompare(b.name.toLowerCase());
          break;
        case 'url':
          compareValue = a.url.toLowerCase().localeCompare(b.url.toLowerCase());
          break;
        case 'type':
          compareValue = a.is_source === b.is_source ? 0 : a.is_source ? -1 : 1;
          break;
      }

      return this.sortAscending ? compareValue : -compareValue;
    });

    return sorted;
  }

  clearMessages(): void {
    setTimeout(() => {
      this.errorMessage = '';
      this.successMessage = '';
    }, 5000);
  }
}
