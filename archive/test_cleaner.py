import re

def clean_doc_text(text):
    # 1. Remove Markdown URLs: [Title](http://...) -> Title
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    
    # 2. Remove HTML tags: <br>, <br/>, <b>, <i>, <ul>, <li>, etc.
    text = re.sub(r'<[^>]+>', '\n', text)
    
    # 3. Clean up HTML entities
    text = text.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    
    # 4. Normalize whitespace
    # Replace multiple spaces with a single space
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        line = re.sub(r'[ \t]+', ' ', line).strip()
        if line:
            cleaned_lines.append(line)
            
    # Join with newlines
    text = '\n'.join(cleaned_lines)
    
    # Convert multiple line breaks into single spaces ? The user said "Converts multiple line breaks into single spaces"
    # But their example kept a newline between Role and Effect.
    # Let's try replacing newlines that don't start with a bullet or uppercase keyword with a space
    final_lines = []
    for line in cleaned_lines:
        if re.match(r'^(@param|Role:|Effect:|Journal:|Product:|Limitations:|Technical Articles:)', line, re.IGNORECASE):
            final_lines.append("\n" + line)
        else:
            final_lines.append(" " + line)
            
    text = "".join(final_lines).strip()
    # clean up any multiple spaces again
    text = re.sub(r'[ \t]+', ' ', text)
    # clean up multiple newlines
    text = re.sub(r'\n\s+', '\n', text).strip()
    
    return text

sample = """
Sets an implicit variable radius blend on each of a list of edges or vertices.
The blend radius is described by one or two variable radius objects.
<br><br>
<b>Technical Articles:</b> <i>[Advanced Blending](http://doc.spatial.com/articles/a/d/v/Component~Advanced_Blending_90cb.html)</i>,
<i>[Blend Attributes](http://doc.spatial.com/articles/b/l/e/Blend_Attributes_568e.html)</i>
<br><br>
<b>Role:</b> Implicit variable radius blends are attached as attributes to
each of the edges or vertices in the list.
<br>
The blend radius is described by the <tt>var_radius</tt> object(s).
<br><br>
Setback at an end of an edge determines where the blend is to be stopped short
of the vertex at the edge end. It is only significant when the vertex is blended.
<br><br>
If start stop angle or end stop angle values are specified, the edge blend is stopped and capped
with a stop plane at the given setback distance. This stop plane is constructed such that the angle
between stop plane and edge direction, about the line passing through end points of blend
cross section, is equal to the specified stop angle value at that end.
A stop angle value of 180 degrees is treated as a special case. In such a case, stop plane is
constructed such that it passes through an end vertex and end points of a blend cross section
at given setback distance.
<br><br>
<b>Limitations:</b> Entity-entity blends cannot create a stopped blend.
The stopping location is based upon the edge being blended; thus, entity-entity blends do not have
this defined location.
<br><br>
<b>Effect:</b> Changes model
<br><br>
<b>Journal:</b> Available
<br><br>
<b>Product(s):</b> 3D ACIS Modeler
<br><br>
@param entities
entities to be blended.
@param left_rad
left radius function.
"""

print(clean_doc_text(sample))
