-- Database Schema for Content Embeddings
-- Using Neon (PostgreSQL) for content storage with vector capabilities

-- Extension for vector storage (for embeddings)
CREATE EXTENSION IF NOT EXISTS vector;

-- Table for textbook content chunks
CREATE TABLE content_chunks (
    id SERIAL PRIMARY KEY,
    chapter_id VARCHAR(255) NOT NULL,
    chunk_text TEXT NOT NULL,
    chunk_type VARCHAR(50), -- 'text', 'code', 'exercise', 'example', etc.
    chunk_metadata JSONB,   -- Additional metadata like section, position, etc.
    embedding vector(1536), -- Assuming OpenAI's ada-002 embedding size
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for chapters (to link with content chunks)
CREATE TABLE chapters (
    id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    learning_objectives TEXT[],
    sections TEXT[],
    exercises_count INTEGER,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for exercises
CREATE TABLE exercises (
    id VARCHAR(255) PRIMARY KEY,
    chapter_id VARCHAR(255) REFERENCES chapters(id),
    content TEXT NOT NULL,
    solution TEXT,
    difficulty VARCHAR(20), -- 'beginner', 'intermediate', 'advanced'
    exercise_type VARCHAR(50), -- 'multiple-choice', 'coding', 'theory', etc.
    related_concepts TEXT[],
    embedding vector(1536),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_content_chunks_chapter_id ON content_chunks(chapter_id);
CREATE INDEX idx_content_chunks_embedding ON content_chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX idx_exercises_chapter_id ON exercises(chapter_id);
CREATE INDEX idx_exercises_embedding ON exercises USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to automatically update the updated_at column
CREATE TRIGGER update_chapters_updated_at 
    BEFORE UPDATE ON chapters 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();