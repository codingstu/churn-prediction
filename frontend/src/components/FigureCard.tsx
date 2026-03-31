import Image from "next/image";

type FigureCardProps = {
  title: string;
  description: string;
  src: string;
  alt: string;
};

export function FigureCard({ title, description, src, alt }: FigureCardProps) {
  return (
    <article className="card card--elevated visual-card">
      <div className="visual-card__header">
        <h3>{title}</h3>
        <p className="muted">{description}</p>
      </div>
      <div className="visual-card__frame">
        <Image
          src={src}
          alt={alt}
          width={1200}
          height={800}
          unoptimized
          className="visual-card__image"
        />
      </div>
    </article>
  );
}
