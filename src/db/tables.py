import sqlalchemy as sa


metadata = sa.MetaData()

short_links = sa.Table(
    'short_link',
    metadata,
    sa.Column(
        'slug',
        sa.String(length=12),
        nullable=False,
        primary_key=True,
    ),
    sa.Column(
        'origin',
        sa.Text,
        nullable=False,
    )
)