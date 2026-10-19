import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { environment } from '../environments/environment';
import {
  COVER_TYPES,
  SAMPLE_VALUES,
  SOIL_TYPES,
  TERRAIN_FEATURES,
  WILDERNESS_AREAS,
} from './feature-schema';

interface PredictionResponse {
  prediction: { id: number; name: string };
  probabilities: Record<string, number>;
  model: string;
  disclaimer: string;
}

@Component({
  selector: 'fc-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class AppComponent implements OnInit {
  private readonly http = inject(HttpClient);

  readonly terrainFeatures = TERRAIN_FEATURES;
  readonly wildernessAreas = WILDERNESS_AREAS;
  readonly soilTypes = SOIL_TYPES;
  readonly coverTypes = COVER_TYPES;
  readonly staticDemo = environment.staticDemo;
  readonly values: Record<string, number> = { ...SAMPLE_VALUES };
  result: PredictionResponse | null = null;
  busy = false;
  apiReady = false;
  errorMessage = '';
  activeSection = 'terrain';

  ngOnInit(): void {
    if (this.staticDemo) return;
    this.http.get<{ model_loaded: boolean }>('/api/health').subscribe({
      next: (health) => (this.apiReady = health.model_loaded),
      error: () => (this.apiReady = false),
    });
  }

  setWilderness(key: string): void {
    for (const area of this.wildernessAreas) this.values[area.key] = Number(area.key === key);
  }

  setSoil(key: string): void {
    for (const soil of this.soilTypes) this.values[soil.key] = Number(soil.key === key);
  }

  get selectedWilderness(): string {
    return this.wildernessAreas.find((area) => this.values[area.key] === 1)?.key ?? '';
  }

  get selectedSoil(): string {
    return this.soilTypes.find((soil) => this.values[soil.key] === 1)?.key ?? '';
  }

  get probabilityRows(): Array<{ id: number; label: string; value: number }> {
    if (!this.result) return [];
    return Object.entries(this.result.probabilities)
      .map(([id, value]) => ({ id: Number(id), label: this.coverTypes[Number(id)], value }))
      .sort((left, right) => right.value - left.value);
  }

  loadSample(): void {
    Object.assign(this.values, SAMPLE_VALUES);
    this.result = null;
    this.errorMessage = '';
  }

  predict(): void {
    this.errorMessage = '';
    this.result = null;
    if (!this.apiReady) {
      this.errorMessage = 'Start the local Flask API and model bundle to run an inference.';
      return;
    }
    this.busy = true;
    this.http.post<PredictionResponse>('/api/predict', this.values).subscribe({
      next: (result) => {
        this.result = result;
        this.busy = false;
      },
      error: (error: { error?: { details?: string[]; error?: string } }) => {
        this.errorMessage = error.error?.details?.join(' ') ?? error.error?.error ?? 'The local model could not process this record.';
        this.busy = false;
      },
    });
  }
}
