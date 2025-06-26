import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RagService {
  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) { }

  sendQuery(query: string, technique: string = 'basic'): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/query`, { query, technique });
  }

  ingestDocument(sourceType: string, file?: File, url?: string): Observable<any> {
    const formData = new FormData();
    formData.append('source_type', sourceType);
    if (file) {
      formData.append('file', file, file.name);
    }
    if (url) {
      formData.append('url', url);
    }
    return this.http.post<any>(`${this.apiUrl}/ingest`, formData);
  }

  sendQueryFile(file: File, technique: string) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('technique', technique);
    return this.http.post<any>(`${this.apiUrl}/query-file`, formData);
  }
}