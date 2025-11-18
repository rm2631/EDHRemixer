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
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'Collection Manager';
  collections: Collection[] = [];
  url: string = '';
  loading: boolean = false;
  errorMessage: string = '';
  successMessage: string = '';
  sortColumn: SortColumn | null = null;
  sortAscending: boolean = true;

  constructor(private apiService: ApiService) {}

  addCollection(): void {
    this.errorMessage = '';
    this.successMessage = '';

    if (!this.url.trim()) {
      this.errorMessage = 'URL cannot be empty.';
      return;
    }

    if (!this.url.toLowerCase().includes('moxfield')) {
      this.errorMessage = 'URL must be a valid Moxfield URL.';
      return;
    }

    this.loading = true;
    this.apiService.getDeckName(this.url).subscribe({
      next: (response) => {
        const newCollection: Collection = {
          name: response.name,
          url: this.url,
          is_source: true
        };
        this.collections.push(newCollection);
        this.url = '';
        this.successMessage = 'Collection added successfully!';
        this.loading = false;
        this.clearMessages();
      },
      error: (error) => {
        this.errorMessage = `Error fetching deck name: ${error.error?.error || error.message}`;
        this.loading = false;
        this.clearMessages();
      }
    });
  }

  deleteCollection(index: number): void {
    const collection = this.sortedCollections()[index];
    const originalIndex = this.collections.indexOf(collection);
    this.collections.splice(originalIndex, 1);
    this.successMessage = `Deleted ${collection.name}`;
    this.clearMessages();
  }

  toggleType(index: number): void {
    const collection = this.sortedCollections()[index];
    const originalIndex = this.collections.indexOf(collection);
    this.collections[originalIndex].is_source = !this.collections[originalIndex].is_source;
  }

  reshuffle(): void {
    this.errorMessage = '';
    this.successMessage = '';

    if (this.collections.length === 0) {
      this.errorMessage = 'No collections to process. Please add some first.';
      this.clearMessages();
      return;
    }

    const hasSources = this.collections.some(c => c.is_source);
    const hasTargets = this.collections.some(c => !c.is_source);

    if (!hasSources) {
      this.errorMessage = 'At least one collection must be a source.';
      this.clearMessages();
      return;
    }

    if (!hasTargets) {
      this.errorMessage = 'At least one collection must be a target.';
      this.clearMessages();
      return;
    }

    this.loading = true;
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
        this.clearMessages();
      },
      error: (error) => {
        this.errorMessage = `Error running the engine: ${error.error?.error || error.message}`;
        this.loading = false;
        this.clearMessages();
      }
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
          compareValue = a.name.toLowerCase().localeCompare(b.name.toLowerCase());
          break;
        case 'url':
          compareValue = a.url.toLowerCase().localeCompare(b.url.toLowerCase());
          break;
        case 'type':
          compareValue = a.is_source === b.is_source ? 0 : (a.is_source ? -1 : 1);
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
