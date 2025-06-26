import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms'; // <-- Add this import
import { AppComponent } from './app.component';
import { RagChatComponent } from './components/rag-chat/rag-chat.component';

@NgModule({
  declarations: [
    AppComponent,
    RagChatComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }