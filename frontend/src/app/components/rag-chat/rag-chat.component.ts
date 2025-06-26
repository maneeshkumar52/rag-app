import { Component } from '@angular/core';
import { RagService } from '../../services/rag.service';
import { catchError } from 'rxjs/operators';
import { of } from 'rxjs';

@Component({
  selector: 'app-rag-chat',
  templateUrl: './rag-chat.component.html',
  styleUrls: ['./rag-chat.component.css']
})
export class RagChatComponent {
  userInput: string = '';
  chatResponses: string[] = [];
  sourceType: string = 'text';
  selectedFile: File | null = null;
  webUrl: string = '';
  selectedQueryFile: File | null = null;
  statusMessage: string = '';
  ragTechnique: string = 'basic'; // NEW

  constructor(private ragService: RagService) { }

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
  }

  ingest() {
    this.statusMessage = 'Ingesting...';
    if (this.sourceType === 'web') {
      this.ragService.ingestDocument(this.sourceType, undefined, this.webUrl)
        .pipe(
          catchError(err => {
            this.statusMessage = 'Ingest failed: ' + (err.error?.detail || err.message || 'Unknown error');
            return of(null);
          })
        )
        .subscribe(res => {
          if (res) {
            this.statusMessage = 'Ingest successful!';
          }
        });
    } else if (this.selectedFile) {
      this.ragService.ingestDocument(this.sourceType, this.selectedFile)
        .pipe(
          catchError(err => {
            this.statusMessage = 'Ingest failed: ' + (err.error?.detail || err.message || 'Unknown error');
            return of(null);
          })
        )
        .subscribe(res => {
          if (res) {
            this.statusMessage = 'Ingest successful!';
          }
        });
    }
  }

  sendMessage() {
    if (!this.userInput) return;
    const userMsg = `You: ${this.userInput}`;
    this.chatResponses.push(userMsg);
    this.statusMessage = 'Querying...';
    const question = this.userInput;
    this.userInput = '';
    this.ragService.sendQuery(question, this.ragTechnique)
      .pipe(
        catchError(err => {
          this.statusMessage = 'Query failed: ' + (err.error?.detail || err.message || 'Unknown error');
          this.chatResponses.push('Bot: ' + this.statusMessage);
          return of(null);
        })
      )
      .subscribe(res => {
        if (res) {
          this.chatResponses.push('Bot: ' + (res.answer || JSON.stringify(res)));
          this.statusMessage = '';
        }
      });
  }


  onQueryFileSelected(event: any) {
    this.selectedQueryFile = event.target.files[0];
  }

  sendQueryFile() {
    if (!this.selectedQueryFile) return;
    this.statusMessage = 'Querying...';
    this.ragService.sendQueryFile(this.selectedQueryFile, this.ragTechnique)
      .pipe(
        catchError(err => {
          this.statusMessage = 'Query failed: ' + (err.error?.detail || err.message || 'Unknown error');
          return of(null);
        })
      )
      .subscribe(res => {
        if (res) {
          this.chatResponses.push(res.answer || JSON.stringify(res));
          this.statusMessage = '';
        }
      });
  }
}