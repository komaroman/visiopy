#!/usr/bin/env python3

import zipfile
import xml.etree.ElementTree as ET
import re
import shutil
import os


class ContentTypes:
    """Holds the content types info [Content_Types].xml"""

    def __init__(self):
        # TODO clean this up
        self.text = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                       <Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
                           <Default Extension="emf" ContentType="image/x-emf"/>
                           <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
                           <Default Extension="xml" ContentType="application/xml"/>
                           <Override PartName="/visio/document.xml" ContentType="application/vnd.ms-visio.drawing.main+xml"/>
                           <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
                           <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
                           <Override PartName="/docProps/custom.xml" ContentType="application/vnd.openxmlformats-officedocument.custom-properties+xml"/>
                           <Override PartName="/visio/masters/masters.xml" ContentType="application/vnd.ms-visio.masters+xml"/>
                           <Override PartName="/visio/masters/master1.xml" ContentType="application/vnd.ms-visio.master+xml"/>
                           <Override PartName="/visio/pages/pages.xml" ContentType="application/vnd.ms-visio.pages+xml"/>
                           <Override PartName="/visio/pages/page1.xml" ContentType="application/vnd.ms-visio.page+xml"/>
                           <Override PartName="/visio/windows.xml" ContentType="application/vnd.ms-visio.windows+xml"/>
                       </Types>"""

    def to_xml(self):
        return self.text


class DocumentRelationships:
    """Holds the relationships for /_rels"""

    def __init__(self):
        # TODO: no chjeating here please!
        self.text = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                     '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
                     '    <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>\n'
                     '    <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/thumbnail" Target="docProps/thumbnail.emf"/>\n'
                     '    <Relationship Id="rId1" Type="http://schemas.microsoft.com/visio/2010/relationships/document" Target="visio/document.xml"/>\n'
                     '    <Relationship Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/custom-properties" Target="docProps/custom.xml"/>\n'
                     '    <Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>\n'
                     '</Relationships>')

    def to_xml(self):
        return self.text


class VisioRelationships:
    """Holds the data for document.xml.rels in visio/_rels folder"""

    def __init__(self):
        # TODO: cheating here and just pasting the text.
        #       we should understand what this does and make a proper
        #       object out of it.
        self.text = ('<?xml version="1.0" encoding="UTF-8" standalone="true"?>\n'
                     '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
                     '    <Relationship Target="windows.xml" Type="http://schemas.microsoft.com/visio/2010/relationships/windows" Id="rId3"/>\n'
                     '    <Relationship Target="pages/pages.xml" Type="http://schemas.microsoft.com/visio/2010/relationships/pages" Id="rId2"/>\n'
                     '    <Relationship Target="masters/masters.xml" Type="http://schemas.microsoft.com/visio/2010/relationships/masters" Id="rId1"/>\n'
                     '</Relationships>')

    def to_xml(self):
        """Generates the raw xml output"""
        return self.text


class WindowsProperties:
    """Class containing data for /visio/windows.xml"""

    def __init__(self):
        # TODO you know the drill, fix this sh1t
        self.text = ("<?xml version='1.0' encoding='utf-8' ?>"
                     "<Windows ClientWidth='1366' ClientHeight='563' xmlns='http://schemas.microsoft.com/office/visio/2012/main' xmlns:r='http://schemas.openxmlformats.org/officeDocument/2006/relationships' xml:space='preserve'>"
                     "<Window ID='0' WindowType='Drawing' WindowState='1073741824' WindowLeft='-8' WindowTop='-30' WindowWidth='1382' WindowHeight='601' ContainerType='Page' Page='0' ViewScale='0.82' ViewCenterX='4.1275082550165' ViewCenterY='8.5852171704343'>"
                     "<ShowRulers>1</ShowRulers>"
                     "<ShowGrid>1</ShowGrid>"
                     "<ShowPageBreaks>0</ShowPageBreaks>"
                     "<ShowGuides>1</ShowGuides>"
                     "<ShowConnectionPoints>1</ShowConnectionPoints>"
                     "<GlueSettings>9</GlueSettings>"
                     "<SnapSettings>65847</SnapSettings>"
                     "<SnapExtensions>34</SnapExtensions>"
                     "<SnapAngles/>"
                     "<DynamicGridEnabled>1</DynamicGridEnabled>"
                     "<TabSplitterPos>0.5</TabSplitterPos>"
                     "</Window>"
                     "</Windows>")

    def to_xml(self):
        return self.text


class DocumentProperties:
    """Class containing data for /visio/document.xml"""

    def __init__(self):
        # TODO, see all todo's above
        self.text = """<?xml version='1.0' encoding='utf-8' ?>
                    <VisioDocument xmlns='http://schemas.microsoft.com/office/visio/2012/main' xmlns:r='http://schemas.openxmlformats.org/officeDocument/2006/relationships' xml:space='preserve'>
                        <DocumentSettings TopPage='0' DefaultTextStyle='3' DefaultLineStyle='3' DefaultFillStyle='3' DefaultGuideStyle='4'>
                            <GlueSettings>9</GlueSettings>
                            <SnapSettings>65847</SnapSettings>
                            <SnapExtensions>34</SnapExtensions>
                            <SnapAngles/>
                            <DynamicGridEnabled>1</DynamicGridEnabled>
                            <ProtectStyles>0</ProtectStyles>
                            <ProtectShapes>0</ProtectShapes>
                            <ProtectMasters>0</ProtectMasters>
                            <ProtectBkgnds>0</ProtectBkgnds>
                        </DocumentSettings>
                        <Colors>
                            <ColorEntry IX='24' RGB='#7F7F7F'/>
                            <ColorEntry IX='25' RGB='#FFFFFF'/>
                        </Colors>
                        <FaceNames>
                            <FaceName NameU='Calibri' UnicodeRanges='-520092929 1073786111 9 0' CharSets='536871327 0' Panose='2 15 5 2 2 2 4 3 2 4' Flags='325'/>
                        </FaceNames>
                        <StyleSheets>
                            <StyleSheet ID='0' NameU='No Style' IsCustomNameU='1' Name='No Style' IsCustomName='1'>
                                <Cell N='EnableLineProps' V='1'/>
                                <Cell N='EnableFillProps' V='1'/>
                                <Cell N='EnableTextProps' V='1'/>
                                <Cell N='HideForApply' V='0'/>
                                <Cell N='LineWeight' V='0.01041666666666667'/>
                                <Cell N='LineColor' V='0'/>
                                <Cell N='LinePattern' V='1'/>
                                <Cell N='Rounding' V='0'/>
                                <Cell N='EndArrowSize' V='2'/>
                                <Cell N='BeginArrow' V='0'/>
                                <Cell N='EndArrow' V='0'/>
                                <Cell N='LineCap' V='0'/>
                                <Cell N='BeginArrowSize' V='2'/>
                                <Cell N='LineColorTrans' V='0'/>
                                <Cell N='CompoundType' V='0'/>
                                <Cell N='FillForegnd' V='1'/>
                                <Cell N='FillBkgnd' V='0'/>
                                <Cell N='FillPattern' V='1'/>
                                <Cell N='ShdwForegnd' V='0'/>
                                <Cell N='ShdwPattern' V='0'/>
                                <Cell N='FillForegndTrans' V='0'/>
                                <Cell N='FillBkgndTrans' V='0'/>
                                <Cell N='ShdwForegndTrans' V='0'/>
                                <Cell N='ShapeShdwType' V='0'/>
                                <Cell N='ShapeShdwOffsetX' V='0'/>
                                <Cell N='ShapeShdwOffsetY' V='0'/>
                                <Cell N='ShapeShdwObliqueAngle' V='0'/>
                                <Cell N='ShapeShdwScaleFactor' V='1'/>
                                <Cell N='ShapeShdwBlur' V='0'/>
                                <Cell N='ShapeShdwShow' V='0'/>
                                <Cell N='LeftMargin' V='0'/>
                                <Cell N='RightMargin' V='0'/>
                                <Cell N='TopMargin' V='0'/>
                                <Cell N='BottomMargin' V='0'/>
                                <Cell N='VerticalAlign' V='1'/>
                                <Cell N='TextBkgnd' V='0'/>
                                <Cell N='DefaultTabStop' V='0.5905511811023622'/>
                                <Cell N='TextDirection' V='0'/>
                                <Cell N='TextBkgndTrans' V='0'/>
                                <Cell N='LockWidth' V='0'/>
                                <Cell N='LockHeight' V='0'/>
                                <Cell N='LockMoveX' V='0'/>
                                <Cell N='LockMoveY' V='0'/>
                                <Cell N='LockAspect' V='0'/>
                                <Cell N='LockDelete' V='0'/>
                                <Cell N='LockBegin' V='0'/>
                                <Cell N='LockEnd' V='0'/>
                                <Cell N='LockRotate' V='0'/>
                                <Cell N='LockCrop' V='0'/>
                                <Cell N='LockVtxEdit' V='0'/>
                                <Cell N='LockTextEdit' V='0'/>
                                <Cell N='LockFormat' V='0'/>
                                <Cell N='LockGroup' V='0'/>
                                <Cell N='LockCalcWH' V='0'/>
                                <Cell N='LockSelect' V='0'/>
                                <Cell N='LockCustProp' V='0'/>
                                <Cell N='LockFromGroupFormat' V='0'/>
                                <Cell N='LockThemeColors' V='0'/>
                                <Cell N='LockThemeEffects' V='0'/>
                                <Cell N='LockThemeConnectors' V='0'/>
                                <Cell N='LockThemeFonts' V='0'/>
                                <Cell N='LockThemeIndex' V='0'/>
                                <Cell N='LockReplace' V='0'/>
                                <Cell N='LockVariation' V='0'/>
                                <Cell N='NoObjHandles' V='0'/>
                                <Cell N='NonPrinting' V='0'/>
                                <Cell N='NoCtlHandles' V='0'/>
                                <Cell N='NoAlignBox' V='0'/>
                                <Cell N='UpdateAlignBox' V='0'/>
                                <Cell N='HideText' V='0'/>
                                <Cell N='DynFeedback' V='0'/>
                                <Cell N='GlueType' V='0'/>
                                <Cell N='WalkPreference' V='0'/>
                                <Cell N='BegTrigger' V='0' F='No Formula'/>
                                <Cell N='EndTrigger' V='0' F='No Formula'/>
                                <Cell N='ObjType' V='0'/>
                                <Cell N='Comment' V=''/>
                                <Cell N='IsDropSource' V='0'/>
                                <Cell N='NoLiveDynamics' V='0'/>
                                <Cell N='LocalizeMerge' V='0'/>
                                <Cell N='NoProofing' V='0'/>
                                <Cell N='Calendar' V='0'/>
                                <Cell N='LangID' V='en-GB'/>
                                <Cell N='ShapeKeywords' V=''/>
                                <Cell N='DropOnPageScale' V='1'/>
                                <Cell N='TheData' V='0' F='No Formula'/>
                                <Cell N='TheText' V='0' F='No Formula'/>
                                <Cell N='EventDblClick' V='0' F='No Formula'/>
                                <Cell N='EventXFMod' V='0' F='No Formula'/>
                                <Cell N='EventDrop' V='0' F='No Formula'/>
                                <Cell N='EventMultiDrop' V='0' F='No Formula'/>
                                <Cell N='HelpTopic' V=''/>
                                <Cell N='Copyright' V=''/>
                                <Cell N='LayerMember' V=''/>
                                <Cell N='XRulerDensity' V='32'/>
                                <Cell N='YRulerDensity' V='32'/>
                                <Cell N='XRulerOrigin' V='0'/>
                                <Cell N='YRulerOrigin' V='0'/>
                                <Cell N='XGridDensity' V='8'/>
                                <Cell N='YGridDensity' V='8'/>
                                <Cell N='XGridSpacing' V='0'/>
                                <Cell N='YGridSpacing' V='0'/>
                                <Cell N='XGridOrigin' V='0'/>
                                <Cell N='YGridOrigin' V='0'/>
                                <Cell N='Gamma' V='1'/>
                                <Cell N='Contrast' V='0.5'/>
                                <Cell N='Brightness' V='0.5'/>
                                <Cell N='Sharpen' V='0'/>
                                <Cell N='Blur' V='0'/>
                                <Cell N='Denoise' V='0'/>
                                <Cell N='Transparency' V='0'/>
                                <Cell N='SelectMode' V='1'/>
                                <Cell N='DisplayMode' V='2'/>
                                <Cell N='IsDropTarget' V='0'/>
                                <Cell N='IsSnapTarget' V='1'/>
                                <Cell N='IsTextEditTarget' V='1'/>
                                <Cell N='DontMoveChildren' V='0'/>
                                <Cell N='ShapePermeableX' V='0'/>
                                <Cell N='ShapePermeableY' V='0'/>
                                <Cell N='ShapePermeablePlace' V='0'/>
                                <Cell N='Relationships' V='0'/>
                                <Cell N='ShapeFixedCode' V='0'/>
                                <Cell N='ShapePlowCode' V='0'/>
                                <Cell N='ShapeRouteStyle' V='0'/>
                                <Cell N='ShapePlaceStyle' V='0'/>
                                <Cell N='ConFixedCode' V='0'/>
                                <Cell N='ConLineJumpCode' V='0'/>
                                <Cell N='ConLineJumpStyle' V='0'/>
                                <Cell N='ConLineJumpDirX' V='0'/>
                                <Cell N='ConLineJumpDirY' V='0'/>
                                <Cell N='ShapePlaceFlip' V='0'/>
                                <Cell N='ConLineRouteExt' V='0'/>
                                <Cell N='ShapeSplit' V='0'/>
                                <Cell N='ShapeSplittable' V='0'/>
                                <Cell N='DisplayLevel' V='0'/>
                                <Cell N='ResizePage' V='0'/>
                                <Cell N='EnableGrid' V='0'/>
                                <Cell N='DynamicsOff' V='0'/>
                                <Cell N='CtrlAsInput' V='0'/>
                                <Cell N='AvoidPageBreaks' V='0'/>
                                <Cell N='PlaceStyle' V='0'/>
                                <Cell N='RouteStyle' V='0'/>
                                <Cell N='PlaceDepth' V='0'/>
                                <Cell N='PlowCode' V='0'/>
                                <Cell N='LineJumpCode' V='1'/>
                                <Cell N='LineJumpStyle' V='0'/>
                                <Cell N='PageLineJumpDirX' V='0'/>
                                <Cell N='PageLineJumpDirY' V='0'/>
                                <Cell N='LineToNodeX' V='0.09842519685039369'/>
                                <Cell N='LineToNodeY' V='0.09842519685039369'/>
                                <Cell N='BlockSizeX' V='0.1968503937007874'/>
                                <Cell N='BlockSizeY' V='0.1968503937007874'/>
                                <Cell N='AvenueSizeX' V='0.2952755905511811'/>
                                <Cell N='AvenueSizeY' V='0.2952755905511811'/>
                                <Cell N='LineToLineX' V='0.09842519685039369'/>
                                <Cell N='LineToLineY' V='0.09842519685039369'/>
                                <Cell N='LineJumpFactorX' V='0.66666666666667'/>
                                <Cell N='LineJumpFactorY' V='0.66666666666667'/>
                                <Cell N='LineAdjustFrom' V='0'/>
                                <Cell N='LineAdjustTo' V='0'/>
                                <Cell N='PlaceFlip' V='0'/>
                                <Cell N='LineRouteExt' V='0'/>
                                <Cell N='PageShapeSplit' V='0'/>
                                <Cell N='PageLeftMargin' V='0.25'/>
                                <Cell N='PageRightMargin' V='0.25'/>
                                <Cell N='PageTopMargin' V='0.25'/>
                                <Cell N='PageBottomMargin' V='0.25'/>
                                <Cell N='ScaleX' V='1'/>
                                <Cell N='ScaleY' V='1'/>
                                <Cell N='PagesX' V='1'/>
                                <Cell N='PagesY' V='1'/>
                                <Cell N='CenterX' V='0'/>
                                <Cell N='CenterY' V='0'/>
                                <Cell N='OnPage' V='0'/>
                                <Cell N='PrintGrid' V='0'/>
                                <Cell N='PrintPageOrientation' V='1'/>
                                <Cell N='PaperKind' V='9'/>
                                <Cell N='PaperSource' V='7'/>
                                <Cell N='QuickStyleLineColor' V='100'/>
                                <Cell N='QuickStyleFillColor' V='100'/>
                                <Cell N='QuickStyleShadowColor' V='100'/>
                                <Cell N='QuickStyleFontColor' V='100'/>
                                <Cell N='QuickStyleLineMatrix' V='100'/>
                                <Cell N='QuickStyleFillMatrix' V='100'/>
                                <Cell N='QuickStyleEffectsMatrix' V='100'/>
                                <Cell N='QuickStyleFontMatrix' V='100'/>
                                <Cell N='QuickStyleType' V='0'/>
                                <Cell N='QuickStyleVariation' V='0'/>
                                <Cell N='LineGradientDir' V='0'/>
                                <Cell N='LineGradientAngle' V='1.5707963267949'/>
                                <Cell N='FillGradientDir' V='0'/>
                                <Cell N='FillGradientAngle' V='1.5707963267949'/>
                                <Cell N='LineGradientEnabled' V='0'/>
                                <Cell N='FillGradientEnabled' V='0'/>
                                <Cell N='RotateGradientWithShape' V='1'/>
                                <Cell N='UseGroupGradient' V='0'/>
                                <Cell N='BevelTopType' V='0'/>
                                <Cell N='BevelTopWidth' V='0'/>
                                <Cell N='BevelTopHeight' V='0'/>
                                <Cell N='BevelBottomType' V='0'/>
                                <Cell N='BevelBottomWidth' V='0'/>
                                <Cell N='BevelBottomHeight' V='0'/>
                                <Cell N='BevelDepthColor' V='1'/>
                                <Cell N='BevelDepthSize' V='0'/>
                                <Cell N='BevelContourColor' V='0'/>
                                <Cell N='BevelContourSize' V='0'/>
                                <Cell N='BevelMaterialType' V='0'/>
                                <Cell N='BevelLightingType' V='0'/>
                                <Cell N='BevelLightingAngle' V='0'/>
                                <Cell N='RotationXAngle' V='0'/>
                                <Cell N='RotationYAngle' V='0'/>
                                <Cell N='RotationZAngle' V='0'/>
                                <Cell N='RotationType' V='0'/>
                                <Cell N='Perspective' V='0'/>
                                <Cell N='DistanceFromGround' V='0'/>
                                <Cell N='KeepTextFlat' V='0'/>
                                <Cell N='ReflectionTrans' V='0'/>
                                <Cell N='ReflectionSize' V='0'/>
                                <Cell N='ReflectionDist' V='0'/>
                                <Cell N='ReflectionBlur' V='0'/>
                                <Cell N='GlowColor' V='1'/>
                                <Cell N='GlowColorTrans' V='0'/>
                                <Cell N='GlowSize' V='0'/>
                                <Cell N='SoftEdgesSize' V='0'/>
                                <Cell N='SketchSeed' V='0'/>
                                <Cell N='SketchEnabled' V='0'/>
                                <Cell N='SketchAmount' V='5'/>
                                <Cell N='SketchLineWeight' V='0.04166666666666666' U='PT'/>
                                <Cell N='SketchLineChange' V='0.14'/>
                                <Cell N='SketchFillChange' V='0.1'/>
                                <Cell N='ColorSchemeIndex' V='0'/>
                                <Cell N='EffectSchemeIndex' V='0'/>
                                <Cell N='ConnectorSchemeIndex' V='0'/>
                                <Cell N='FontSchemeIndex' V='0'/>
                                <Cell N='ThemeIndex' V='0'/>
                                <Cell N='VariationColorIndex' V='0'/>
                                <Cell N='VariationStyleIndex' V='0'/>
                                <Cell N='EmbellishmentIndex' V='0'/>
                                <Cell N='ReplaceLockShapeData' V='0'/>
                                <Cell N='ReplaceLockText' V='0'/>
                                <Cell N='ReplaceLockFormat' V='0'/>
                                <Cell N='ReplaceCopyCells' V='0' U='BOOL' F='No Formula'/>
                                <Cell N='PageWidth' V='0' F='No Formula'/>
                                <Cell N='PageHeight' V='0' F='No Formula'/>
                                <Cell N='ShdwOffsetX' V='0' F='No Formula'/>
                                <Cell N='ShdwOffsetY' V='0' F='No Formula'/>
                                <Cell N='PageScale' V='0' U='MM' F='No Formula'/>
                                <Cell N='DrawingScale' V='0' U='MM' F='No Formula'/>
                                <Cell N='DrawingSizeType' V='0' F='No Formula'/>
                                <Cell N='DrawingScaleType' V='0' F='No Formula'/>
                                <Cell N='InhibitSnap' V='0' F='No Formula'/>
                                <Cell N='PageLockReplace' V='0' U='BOOL' F='No Formula'/>
                                <Cell N='PageLockDuplicate' V='0' U='BOOL' F='No Formula'/>
                                <Cell N='UIVisibility' V='0' F='No Formula'/>
                                <Cell N='ShdwType' V='0' F='No Formula'/>
                                <Cell N='ShdwObliqueAngle' V='0' F='No Formula'/>
                                <Cell N='ShdwScaleFactor' V='0' F='No Formula'/>
                                <Cell N='DrawingResizeType' V='0' F='No Formula'/>
                                <Section N='Character'>
                                    <Row IX='0'>
                                        <Cell N='Font' V='Calibri'/>
                                        <Cell N='Color' V='0'/>
                                        <Cell N='Style' V='0'/>
                                        <Cell N='Case' V='0'/>
                                        <Cell N='Pos' V='0'/>
                                        <Cell N='FontScale' V='1'/>
                                        <Cell N='Size' V='0.1666666666666667'/>
                                        <Cell N='DblUnderline' V='0'/>
                                        <Cell N='Overline' V='0'/>
                                        <Cell N='Strikethru' V='0'/>
                                        <Cell N='DoubleStrikethrough' V='0'/>
                                        <Cell N='Letterspace' V='0'/>
                                        <Cell N='ColorTrans' V='0'/>
                                        <Cell N='AsianFont' V='0'/>
                                        <Cell N='ComplexScriptFont' V='0'/>
                                        <Cell N='ComplexScriptSize' V='-1'/>
                                        <Cell N='LangID' V='en-GB'/>
                                    </Row>
                                </Section>
                                <Section N='Paragraph'>
                                    <Row IX='0'>
                                        <Cell N='IndFirst' V='0'/>
                                        <Cell N='IndLeft' V='0'/>
                                        <Cell N='IndRight' V='0'/>
                                        <Cell N='SpLine' V='-1.2'/>
                                        <Cell N='SpBefore' V='0'/>
                                        <Cell N='SpAfter' V='0'/>
                                        <Cell N='HorzAlign' V='1'/>
                                        <Cell N='Bullet' V='0'/>
                                        <Cell N='BulletStr' V=''/>
                                        <Cell N='BulletFont' V='0'/>
                                        <Cell N='BulletFontSize' V='-1'/>
                                        <Cell N='TextPosAfterBullet' V='0'/>
                                        <Cell N='Flags' V='0'/>
                                    </Row>
                                </Section>
                                <Section N='Tabs'>
                                    <Row IX='0'/>
                                </Section>
                                <Section N='LineGradient'>
                                    <Row IX='0'>
                                        <Cell N='GradientStopColor' V='1'/>
                                        <Cell N='GradientStopColorTrans' V='0'/>
                                        <Cell N='GradientStopPosition' V='0'/>
                                    </Row>
                                </Section>
                                <Section N='FillGradient'>
                                    <Row IX='0'>
                                        <Cell N='GradientStopColor' V='1'/>
                                        <Cell N='GradientStopColorTrans' V='0'/>
                                        <Cell N='GradientStopPosition' V='0'/>
                                    </Row>
                                </Section>
                            </StyleSheet>
                            <StyleSheet ID='1' NameU='Text Only' IsCustomNameU='1' Name='Text Only' IsCustomName='1' LineStyle='3' FillStyle='3' TextStyle='3'>
                                <Cell N='EnableLineProps' V='1'/>
                                <Cell N='EnableFillProps' V='1'/>
                                <Cell N='EnableTextProps' V='1'/>
                                <Cell N='HideForApply' V='0'/>
                                <Cell N='LineWeight' V='Themed' F='Inh'/>
                                <Cell N='LineColor' V='Themed' F='Inh'/>
                                <Cell N='LinePattern' V='Themed' F='Inh'/>
                                <Cell N='Rounding' V='Themed' F='Inh'/>
                                <Cell N='EndArrowSize' V='2' F='Inh'/>
                                <Cell N='BeginArrow' V='0' F='Inh'/>
                                <Cell N='EndArrow' V='0' F='Inh'/>
                                <Cell N='LineCap' V='Themed' F='Inh'/>
                                <Cell N='BeginArrowSize' V='2' F='Inh'/>
                                <Cell N='LineColorTrans' V='Themed' F='Inh'/>
                                <Cell N='CompoundType' V='Themed' F='Inh'/>
                                <Cell N='FillForegnd' V='Themed' F='Inh'/>
                                <Cell N='FillBkgnd' V='Themed' F='Inh'/>
                                <Cell N='FillPattern' V='Themed' F='Inh'/>
                                <Cell N='ShdwForegnd' V='Themed' F='Inh'/>
                                <Cell N='ShdwPattern' V='Themed' F='Inh'/>
                                <Cell N='FillForegndTrans' V='Themed' F='Inh'/>
                                <Cell N='FillBkgndTrans' V='Themed' F='Inh'/>
                                <Cell N='ShdwForegndTrans' V='Themed' F='Inh'/>
                                <Cell N='ShapeShdwType' V='Themed' F='Inh'/>
                                <Cell N='ShapeShdwOffsetX' V='Themed' F='Inh'/>
                                <Cell N='ShapeShdwOffsetY' V='Themed' F='Inh'/>
                                <Cell N='ShapeShdwObliqueAngle' V='Themed' F='Inh'/>
                                <Cell N='ShapeShdwScaleFactor' V='Themed' F='Inh'/>
                                <Cell N='ShapeShdwBlur' V='Themed' F='Inh'/>
                                <Cell N='ShapeShdwShow' V='0' F='Inh'/>
                                <Cell N='LeftMargin' V='0'/>
                                <Cell N='RightMargin' V='0'/>
                                <Cell N='TopMargin' V='0'/>
                                <Cell N='BottomMargin' V='0'/>
                                <Cell N='VerticalAlign' V='0'/>
                                <Cell N='TextBkgnd' V='0'/>
                                <Cell N='DefaultTabStop' V='0.5905511811023622' F='Inh'/>
                                <Cell N='TextDirection' V='0' F='Inh'/>
                                <Cell N='TextBkgndTrans' V='0' F='Inh'/>
                                <Cell N='LineGradientDir' V='Themed' F='Inh'/>
                                <Cell N='LineGradientAngle' V='Themed' F='Inh'/>
                                <Cell N='FillGradientDir' V='Themed' F='Inh'/>
                                <Cell N='FillGradientAngle' V='Themed' F='Inh'/>
                                <Cell N='LineGradientEnabled' V='Themed' F='Inh'/>
                                <Cell N='FillGradientEnabled' V='0' F='Inh'/>
                                <Cell N='RotateGradientWithShape' V='Themed' F='Inh'/>
                                <Cell N='UseGroupGradient' V='Themed' F='Inh'/>
                                <Section N='Paragraph'>
                                    <Row IX='0'>
                                        <Cell N='IndFirst' V='0' F='Inh'/>
                                        <Cell N='IndLeft' V='0' F='Inh'/>
                                        <Cell N='IndRight' V='0' F='Inh'/>
                                        <Cell N='SpLine' V='-1.2' F='Inh'/>
                                        <Cell N='SpBefore' V='0' F='Inh'/>
                                        <Cell N='SpAfter' V='0' F='Inh'/>
                                        <Cell N='HorzAlign' V='0'/>
                                        <Cell N='Bullet' V='0' F='Inh'/>
                                        <Cell N='BulletStr' V='' F='Inh'/>
                                        <Cell N='BulletFont' V='0' F='Inh'/>
                                        <Cell N='BulletFontSize' V='-1' F='Inh'/>
                                        <Cell N='TextPosAfterBullet' V='0' F='Inh'/>
                                        <Cell N='Flags' V='0' F='Inh'/>
                                    </Row>
                                </Section>
                            </StyleSheet>
                            <StyleSheet ID='2' NameU='None' IsCustomNameU='1' Name='None' IsCustomName='1' LineStyle='3' FillStyle='3' TextStyle='3'>
                                <Cell N='EnableLineProps' V='1'/>
                                <Cell N='EnableFillProps' V='1'/>
                                <Cell N='EnableTextProps' V='1'/>
                                <Cell N='HideForApply' V='0'/>
                                <Cell N='LineWeight' V='Themed' F='Inh'/>
                                <Cell N='LineColor' V='Themed' F='Inh'/>
                                <Cell N='LinePattern' V='0'/>
                                <Cell N='Rounding' V='Themed' F='Inh'/>
                                <Cell N='EndArrowSize' V='2' F='Inh'/>
                                <Cell N='BeginArrow' V='0' F='Inh'/>
                                <Cell N='EndArrow' V='0' F='Inh'/>
                                <Cell N='LineCap' V='Themed' F='Inh'/>
                                <Cell N='BeginArrowSize' V='2' F='Inh'/>
                                <Cell N='LineColorTrans' V='Themed' F='Inh'/>
                                <Cell N='CompoundType' V='Themed' F='Inh'/>
                                <Cell N='FillForegnd' V='Themed' F='Inh'/>
                                <Cell N='FillBkgnd' V='Themed' F='Inh'/>
                                <Cell N='FillPattern' V='0'/>
                                <Cell N='ShdwForegnd' V='Themed' F='Inh'/>
                                <Cell N='ShdwPattern' V='Themed' F='Inh'/>
                                <Cell N='FillForegndTrans' V='Themed' F='Inh'/>
                                <Cell N='FillBkgndTrans' V='Themed' F='Inh'/>
                                <Cell N='ShdwForegndTrans' V='Themed' F='Inh'/>
                                <Cell N='ShapeShdwType' V='Themed' F='Inh'/>
                                <Cell N='ShapeShdwOffsetX' V='Themed' F='Inh'/>
                                <Cell N='ShapeShdwOffsetY' V='Themed' F='Inh'/>
                                <Cell N='ShapeShdwObliqueAngle' V='Themed' F='Inh'/>
                                <Cell N='ShapeShdwScaleFactor' V='Themed' F='Inh'/>
                                <Cell N='ShapeShdwBlur' V='Themed' F='Inh'/>
                                <Cell N='ShapeShdwShow' V='0' F='Inh'/>
                                <Cell N='LineGradientDir' V='Themed' F='Inh'/>
                                <Cell N='LineGradientAngle' V='Themed' F='Inh'/>
                                <Cell N='FillGradientDir' V='Themed' F='Inh'/>
                                <Cell N='FillGradientAngle' V='Themed' F='Inh'/>
                                <Cell N='LineGradientEnabled' V='0'/>
                                <Cell N='FillGradientEnabled' V='0'/>
                                <Cell N='RotateGradientWithShape' V='Themed' F='Inh'/>
                                <Cell N='UseGroupGradient' V='Themed' F='Inh'/>
                                <Cell N='QuickStyleLineColor' V='100' F='Inh'/>
                                <Cell N='QuickStyleFillColor' V='100' F='Inh'/>
                                <Cell N='QuickStyleShadowColor' V='100' F='Inh'/>
                                <Cell N='QuickStyleFontColor' V='100' F='Inh'/>
                                <Cell N='QuickStyleLineMatrix' V='100' F='Inh'/>
                                <Cell N='QuickStyleFillMatrix' V='100' F='Inh'/>
                                <Cell N='QuickStyleEffectsMatrix' V='0' F='GUARD(0)'/>
                                <Cell N='QuickStyleFontMatrix' V='100' F='Inh'/>
                                <Cell N='QuickStyleType' V='0' F='Inh'/>
                                <Cell N='QuickStyleVariation' V='2'/>
                            </StyleSheet>
                            <StyleSheet ID='3' NameU='Normal' IsCustomNameU='1' Name='Normal' IsCustomName='1' LineStyle='6' FillStyle='6' TextStyle='6'>
                                <Cell N='EnableLineProps' V='1'/>
                                <Cell N='EnableFillProps' V='1'/>
                                <Cell N='EnableTextProps' V='1'/>
                                <Cell N='HideForApply' V='0'/>
                                <Cell N='LeftMargin' V='0.05555555555555555' U='PT'/>
                                <Cell N='RightMargin' V='0.05555555555555555' U='PT'/>
                                <Cell N='TopMargin' V='0.05555555555555555' U='PT'/>
                                <Cell N='BottomMargin' V='0.05555555555555555' U='PT'/>
                                <Cell N='VerticalAlign' V='1' F='Inh'/>
                                <Cell N='TextBkgnd' V='0' F='Inh'/>
                                <Cell N='DefaultTabStop' V='0.5905511811023622' F='Inh'/>
                                <Cell N='TextDirection' V='0' F='Inh'/>
                                <Cell N='TextBkgndTrans' V='0' F='Inh'/>
                            </StyleSheet>
                            <StyleSheet ID='4' NameU='Guide' IsCustomNameU='1' Name='Guide' IsCustomName='1' LineStyle='3' FillStyle='3' TextStyle='3'>
                                <Cell N='EnableLineProps' V='1'/>
                                <Cell N='EnableFillProps' V='1'/>
                                <Cell N='EnableTextProps' V='1'/>
                                <Cell N='HideForApply' V='0'/>
                                <Cell N='LineWeight' V='0' U='PT'/>
                                <Cell N='LineColor' V='#7f7f7f'/>
                                <Cell N='LinePattern' V='23'/>
                                <Cell N='Rounding' V='Themed' F='Inh'/>
                                <Cell N='EndArrowSize' V='2' F='Inh'/>
                                <Cell N='BeginArrow' V='0' F='Inh'/>
                                <Cell N='EndArrow' V='0' F='Inh'/>
                                <Cell N='LineCap' V='Themed' F='Inh'/>
                                <Cell N='BeginArrowSize' V='2' F='Inh'/>
                                <Cell N='LineColorTrans' V='Themed' F='Inh'/>
                                <Cell N='CompoundType' V='Themed' F='Inh'/>
                                <Cell N='FillForegnd' V='Themed' F='Inh'/>
                                <Cell N='FillBkgnd' V='Themed' F='Inh'/>
                                <Cell N='FillPattern' V='0'/>
                                <Cell N='ShdwForegnd' V='Themed' F='Inh'/>
                                <Cell N='ShdwPattern' V='Themed' F='Inh'/>
                                <Cell N='FillForegndTrans' V='Themed' F='Inh'/>
                                <Cell N='FillBkgndTrans' V='Themed' F='Inh'/>
                                <Cell N='ShdwForegndTrans' V='Themed' F='Inh'/>
                                <Cell N='ShapeShdwType' V='Themed' F='Inh'/>
                                <Cell N='ShapeShdwOffsetX' V='Themed' F='Inh'/>
                                <Cell N='ShapeShdwOffsetY' V='Themed' F='Inh'/>
                                <Cell N='ShapeShdwObliqueAngle' V='Themed' F='Inh'/>
                                <Cell N='ShapeShdwScaleFactor' V='Themed' F='Inh'/>
                                <Cell N='ShapeShdwBlur' V='Themed' F='Inh'/>
                                <Cell N='ShapeShdwShow' V='0' F='Inh'/>
                                <Cell N='LineGradientDir' V='Themed' F='Inh'/>
                                <Cell N='LineGradientAngle' V='Themed' F='Inh'/>
                                <Cell N='FillGradientDir' V='Themed' F='Inh'/>
                                <Cell N='FillGradientAngle' V='Themed' F='Inh'/>
                                <Cell N='LineGradientEnabled' V='0'/>
                                <Cell N='FillGradientEnabled' V='0'/>
                                <Cell N='RotateGradientWithShape' V='Themed' F='Inh'/>
                                <Cell N='UseGroupGradient' V='Themed' F='Inh'/>
                                <Cell N='LeftMargin' V='0.05555555555555555' U='PT' F='Inh'/>
                                <Cell N='RightMargin' V='0.05555555555555555' U='PT' F='Inh'/>
                                <Cell N='TopMargin' V='0'/>
                                <Cell N='BottomMargin' V='0'/>
                                <Cell N='VerticalAlign' V='2'/>
                                <Cell N='TextBkgnd' V='0' F='Inh'/>
                                <Cell N='DefaultTabStop' V='0.5905511811023622' F='Inh'/>
                                <Cell N='TextDirection' V='0' F='Inh'/>
                                <Cell N='TextBkgndTrans' V='0' F='Inh'/>
                                <Cell N='NoObjHandles' V='0' F='Inh'/>
                                <Cell N='NonPrinting' V='1'/>
                                <Cell N='NoCtlHandles' V='0' F='Inh'/>
                                <Cell N='NoAlignBox' V='0' F='Inh'/>
                                <Cell N='UpdateAlignBox' V='0' F='Inh'/>
                                <Cell N='HideText' V='0' F='Inh'/>
                                <Cell N='DynFeedback' V='0' F='Inh'/>
                                <Cell N='GlueType' V='0' F='Inh'/>
                                <Cell N='WalkPreference' V='0' F='Inh'/>
                                <Cell N='BegTrigger' V='0' F='No Formula'/>
                                <Cell N='EndTrigger' V='0' F='No Formula'/>
                                <Cell N='ObjType' V='0' F='Inh'/>
                                <Cell N='Comment' V='' F='Inh'/>
                                <Cell N='IsDropSource' V='0' F='Inh'/>
                                <Cell N='NoLiveDynamics' V='0' F='Inh'/>
                                <Cell N='LocalizeMerge' V='0' F='Inh'/>
                                <Cell N='NoProofing' V='0' F='Inh'/>
                                <Cell N='Calendar' V='0' F='Inh'/>
                                <Cell N='LangID' V='en-GB' F='Inh'/>
                                <Cell N='ShapeKeywords' V='' F='Inh'/>
                                <Cell N='DropOnPageScale' V='1' F='Inh'/>
                                <Cell N='ShapePermeableX' V='1'/>
                                <Cell N='ShapePermeableY' V='1'/>
                                <Cell N='ShapePermeablePlace' V='1'/>
                                <Cell N='Relationships' V='0' F='Inh'/>
                                <Cell N='ShapeFixedCode' V='0' F='Inh'/>
                                <Cell N='ShapePlowCode' V='0' F='Inh'/>
                                <Cell N='ShapeRouteStyle' V='0' F='Inh'/>
                                <Cell N='ShapePlaceStyle' V='0' F='Inh'/>
                                <Cell N='ConFixedCode' V='0' F='Inh'/>
                                <Cell N='ConLineJumpCode' V='0' F='Inh'/>
                                <Cell N='ConLineJumpStyle' V='0' F='Inh'/>
                                <Cell N='ConLineJumpDirX' V='0' F='Inh'/>
                                <Cell N='ConLineJumpDirY' V='0' F='Inh'/>
                                <Cell N='ShapePlaceFlip' V='0' F='Inh'/>
                                <Cell N='ConLineRouteExt' V='0' F='Inh'/>
                                <Cell N='ShapeSplit' V='0' F='Inh'/>
                                <Cell N='ShapeSplittable' V='0' F='Inh'/>
                                <Cell N='DisplayLevel' V='0' F='Inh'/>
                                <Section N='Character'>
                                    <Row IX='0'>
                                        <Cell N='Font' V='Themed' F='Inh'/>
                                        <Cell N='Color' V='4'/>
                                        <Cell N='Style' V='Themed' F='Inh'/>
                                        <Cell N='Case' V='0' F='Inh'/>
                                        <Cell N='Pos' V='0' F='Inh'/>
                                        <Cell N='FontScale' V='1' F='Inh'/>
                                        <Cell N='Size' V='0.125'/>
                                        <Cell N='DblUnderline' V='0' F='Inh'/>
                                        <Cell N='Overline' V='0' F='Inh'/>
                                        <Cell N='Strikethru' V='0' F='Inh'/>
                                        <Cell N='DoubleStrikethrough' V='0' F='Inh'/>
                                        <Cell N='Letterspace' V='0' F='Inh'/>
                                        <Cell N='ColorTrans' V='0' F='Inh'/>
                                        <Cell N='AsianFont' V='Themed' F='Inh'/>
                                        <Cell N='ComplexScriptFont' V='Themed' F='Inh'/>
                                        <Cell N='ComplexScriptSize' V='-1' F='Inh'/>
                                        <Cell N='LangID' V='en-GB' F='Inh'/>
                                    </Row>
                                </Section>
                            </StyleSheet>
                            <StyleSheet ID='6' NameU='Theme' IsCustomNameU='1' Name='Theme' IsCustomName='1' LineStyle='0' FillStyle='0' TextStyle='0'>
                                <Cell N='EnableLineProps' V='1'/>
                                <Cell N='EnableFillProps' V='1'/>
                                <Cell N='EnableTextProps' V='1'/>
                                <Cell N='HideForApply' V='0'/>
                                <Cell N='LineWeight' V='Themed' F='THEMEVAL()'/>
                                <Cell N='LineColor' V='Themed' F='THEMEVAL()'/>
                                <Cell N='LinePattern' V='Themed' F='THEMEVAL()'/>
                                <Cell N='Rounding' V='Themed' F='THEMEVAL()'/>
                                <Cell N='EndArrowSize' V='2' F='Inh'/>
                                <Cell N='BeginArrow' V='0' F='Inh'/>
                                <Cell N='EndArrow' V='0' F='Inh'/>
                                <Cell N='LineCap' V='Themed' F='THEMEVAL()'/>
                                <Cell N='BeginArrowSize' V='2' F='Inh'/>
                                <Cell N='LineColorTrans' V='Themed' F='THEMEVAL()'/>
                                <Cell N='CompoundType' V='Themed' F='THEMEVAL()'/>
                                <Cell N='FillForegnd' V='Themed' F='THEMEVAL()'/>
                                <Cell N='FillBkgnd' V='Themed' F='THEMEVAL()'/>
                                <Cell N='FillPattern' V='Themed' F='THEMEVAL()'/>
                                <Cell N='ShdwForegnd' V='Themed' F='THEMEVAL()'/>
                                <Cell N='ShdwPattern' V='Themed' F='THEMEVAL()'/>
                                <Cell N='FillForegndTrans' V='Themed' F='THEMEVAL()'/>
                                <Cell N='FillBkgndTrans' V='Themed' F='THEMEVAL()'/>
                                <Cell N='ShdwForegndTrans' V='Themed' F='THEMEVAL()'/>
                                <Cell N='ShapeShdwType' V='Themed' F='THEMEVAL()'/>
                                <Cell N='ShapeShdwOffsetX' V='Themed' F='THEMEVAL()'/>
                                <Cell N='ShapeShdwOffsetY' V='Themed' F='THEMEVAL()'/>
                                <Cell N='ShapeShdwObliqueAngle' V='Themed' F='THEMEVAL()'/>
                                <Cell N='ShapeShdwScaleFactor' V='Themed' F='THEMEVAL()'/>
                                <Cell N='ShapeShdwBlur' V='Themed' F='THEMEVAL()'/>
                                <Cell N='ShapeShdwShow' V='0' F='Inh'/>
                                <Cell N='LineGradientDir' V='Themed' F='THEMEVAL()'/>
                                <Cell N='LineGradientAngle' V='Themed' F='THEMEVAL()'/>
                                <Cell N='FillGradientDir' V='Themed' F='THEMEVAL()'/>
                                <Cell N='FillGradientAngle' V='Themed' F='THEMEVAL()'/>
                                <Cell N='LineGradientEnabled' V='Themed' F='THEMEVAL()'/>
                                <Cell N='FillGradientEnabled' V='0'/>
                                <Cell N='RotateGradientWithShape' V='Themed' F='THEMEVAL()'/>
                                <Cell N='UseGroupGradient' V='Themed' F='THEMEVAL()'/>
                                <Cell N='BevelTopType' V='Themed' F='THEMEVAL()'/>
                                <Cell N='BevelTopWidth' V='Themed' F='THEMEVAL()'/>
                                <Cell N='BevelTopHeight' V='Themed' F='THEMEVAL()'/>
                                <Cell N='BevelBottomType' V='0' F='Inh'/>
                                <Cell N='BevelBottomWidth' V='0' F='Inh'/>
                                <Cell N='BevelBottomHeight' V='0' F='Inh'/>
                                <Cell N='BevelDepthColor' V='1' F='Inh'/>
                                <Cell N='BevelDepthSize' V='0' F='Inh'/>
                                <Cell N='BevelContourColor' V='Themed' F='THEMEVAL()'/>
                                <Cell N='BevelContourSize' V='Themed' F='THEMEVAL()'/>
                                <Cell N='BevelMaterialType' V='Themed' F='THEMEVAL()'/>
                                <Cell N='BevelLightingType' V='Themed' F='THEMEVAL()'/>
                                <Cell N='BevelLightingAngle' V='Themed' F='THEMEVAL()'/>
                                <Cell N='ReflectionTrans' V='Themed' F='THEMEVAL()'/>
                                <Cell N='ReflectionSize' V='Themed' F='THEMEVAL()'/>
                                <Cell N='ReflectionDist' V='Themed' F='THEMEVAL()'/>
                                <Cell N='ReflectionBlur' V='Themed' F='THEMEVAL()'/>
                                <Cell N='GlowColor' V='Themed' F='THEMEVAL()'/>
                                <Cell N='GlowColorTrans' V='Themed' F='THEMEVAL()'/>
                                <Cell N='GlowSize' V='Themed' F='THEMEVAL()'/>
                                <Cell N='SoftEdgesSize' V='Themed' F='THEMEVAL()'/>
                                <Cell N='SketchSeed' V='0' F='Inh'/>
                                <Cell N='SketchEnabled' V='Themed' F='THEMEVAL()'/>
                                <Cell N='SketchAmount' V='Themed' F='THEMEVAL()'/>
                                <Cell N='SketchLineWeight' V='Themed' F='THEMEVAL()'/>
                                <Cell N='SketchLineChange' V='Themed' F='THEMEVAL()'/>
                                <Cell N='SketchFillChange' V='Themed' F='THEMEVAL()'/>
                                <Cell N='QuickStyleLineColor' V='100'/>
                                <Cell N='QuickStyleFillColor' V='100'/>
                                <Cell N='QuickStyleShadowColor' V='100'/>
                                <Cell N='QuickStyleFontColor' V='100'/>
                                <Cell N='QuickStyleLineMatrix' V='100'/>
                                <Cell N='QuickStyleFillMatrix' V='100'/>
                                <Cell N='QuickStyleEffectsMatrix' V='100'/>
                                <Cell N='QuickStyleFontMatrix' V='100'/>
                                <Cell N='QuickStyleType' V='0' F='Inh'/>
                                <Cell N='QuickStyleVariation' V='0' F='Inh'/>
                                <Cell N='ColorSchemeIndex' V='65534'/>
                                <Cell N='EffectSchemeIndex' V='65534'/>
                                <Cell N='ConnectorSchemeIndex' V='65534'/>
                                <Cell N='FontSchemeIndex' V='65534'/>
                                <Cell N='ThemeIndex' V='65534'/>
                                <Cell N='VariationColorIndex' V='65534'/>
                                <Cell N='VariationStyleIndex' V='65534'/>
                                <Cell N='EmbellishmentIndex' V='65534'/>
                                <Section N='Character'>
                                    <Row IX='0'>
                                        <Cell N='Font' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='Color' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='Style' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='Case' V='0' F='Inh'/>
                                        <Cell N='Pos' V='0' F='Inh'/>
                                        <Cell N='FontScale' V='1' F='Inh'/>
                                        <Cell N='Size' V='0.1666666666666667' F='Inh'/>
                                        <Cell N='DblUnderline' V='0' F='Inh'/>
                                        <Cell N='Overline' V='0' F='Inh'/>
                                        <Cell N='Strikethru' V='0' F='Inh'/>
                                        <Cell N='DoubleStrikethrough' V='0' F='Inh'/>
                                        <Cell N='Letterspace' V='0' F='Inh'/>
                                        <Cell N='ColorTrans' V='0' F='Inh'/>
                                        <Cell N='AsianFont' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='ComplexScriptFont' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='ComplexScriptSize' V='-1' F='Inh'/>
                                        <Cell N='LangID' V='en-GB' F='Inh'/>
                                    </Row>
                                </Section>
                                <Section N='FillGradient'>
                                    <Row IX='0'>
                                        <Cell N='GradientStopColor' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopColorTrans' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopPosition' V='Themed' F='THEMEVAL()'/>
                                    </Row>
                                    <Row IX='1'>
                                        <Cell N='GradientStopColor' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopColorTrans' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopPosition' V='Themed' F='THEMEVAL()'/>
                                    </Row>
                                    <Row IX='2'>
                                        <Cell N='GradientStopColor' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopColorTrans' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopPosition' V='Themed' F='THEMEVAL()'/>
                                    </Row>
                                    <Row IX='3'>
                                        <Cell N='GradientStopColor' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopColorTrans' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopPosition' V='Themed' F='THEMEVAL()'/>
                                    </Row>
                                    <Row IX='4'>
                                        <Cell N='GradientStopColor' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopColorTrans' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopPosition' V='Themed' F='THEMEVAL()'/>
                                    </Row>
                                    <Row IX='5'>
                                        <Cell N='GradientStopColor' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopColorTrans' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopPosition' V='Themed' F='THEMEVAL()'/>
                                    </Row>
                                    <Row IX='6'>
                                        <Cell N='GradientStopColor' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopColorTrans' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopPosition' V='Themed' F='THEMEVAL()'/>
                                    </Row>
                                    <Row IX='7'>
                                        <Cell N='GradientStopColor' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopColorTrans' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopPosition' V='Themed' F='THEMEVAL()'/>
                                    </Row>
                                    <Row IX='8'>
                                        <Cell N='GradientStopColor' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopColorTrans' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopPosition' V='Themed' F='THEMEVAL()'/>
                                    </Row>
                                    <Row IX='9'>
                                        <Cell N='GradientStopColor' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopColorTrans' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopPosition' V='Themed' F='THEMEVAL()'/>
                                    </Row>
                                </Section>
                                <Section N='LineGradient'>
                                    <Row IX='0'>
                                        <Cell N='GradientStopColor' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopColorTrans' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopPosition' V='Themed' F='THEMEVAL()'/>
                                    </Row>
                                    <Row IX='1'>
                                        <Cell N='GradientStopColor' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopColorTrans' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopPosition' V='Themed' F='THEMEVAL()'/>
                                    </Row>
                                    <Row IX='2'>
                                        <Cell N='GradientStopColor' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopColorTrans' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopPosition' V='Themed' F='THEMEVAL()'/>
                                    </Row>
                                    <Row IX='3'>
                                        <Cell N='GradientStopColor' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopColorTrans' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopPosition' V='Themed' F='THEMEVAL()'/>
                                    </Row>
                                    <Row IX='4'>
                                        <Cell N='GradientStopColor' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopColorTrans' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopPosition' V='Themed' F='THEMEVAL()'/>
                                    </Row>
                                    <Row IX='5'>
                                        <Cell N='GradientStopColor' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopColorTrans' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopPosition' V='Themed' F='THEMEVAL()'/>
                                    </Row>
                                    <Row IX='6'>
                                        <Cell N='GradientStopColor' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopColorTrans' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopPosition' V='Themed' F='THEMEVAL()'/>
                                    </Row>
                                    <Row IX='7'>
                                        <Cell N='GradientStopColor' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopColorTrans' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopPosition' V='Themed' F='THEMEVAL()'/>
                                    </Row>
                                    <Row IX='8'>
                                        <Cell N='GradientStopColor' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopColorTrans' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopPosition' V='Themed' F='THEMEVAL()'/>
                                    </Row>
                                    <Row IX='9'>
                                        <Cell N='GradientStopColor' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopColorTrans' V='Themed' F='THEMEVAL()'/>
                                        <Cell N='GradientStopPosition' V='Themed' F='THEMEVAL()'/>
                                    </Row>
                                </Section>
                            </StyleSheet>
                            <StyleSheet ID='7' NameU='Connector' IsCustomNameU='1' Name='Connector' IsCustomName='1' LineStyle='3' FillStyle='3' TextStyle='3'>
                                <Cell N='EnableLineProps' V='1'/>
                                <Cell N='EnableFillProps' V='1'/>
                                <Cell N='EnableTextProps' V='1'/>
                                <Cell N='HideForApply' V='0'/>
                                <Cell N='LeftMargin' V='0.05555555555555555' U='PT' F='Inh'/>
                                <Cell N='RightMargin' V='0.05555555555555555' U='PT' F='Inh'/>
                                <Cell N='TopMargin' V='0.05555555555555555' U='PT' F='Inh'/>
                                <Cell N='BottomMargin' V='0.05555555555555555' U='PT' F='Inh'/>
                                <Cell N='VerticalAlign' V='1' F='Inh'/>
                                <Cell N='TextBkgnd' V='#ffffff' F='THEMEGUARD(THEMEVAL("BackgroundColor")+1)'/>
                                <Cell N='DefaultTabStop' V='0.5905511811023622' F='Inh'/>
                                <Cell N='TextDirection' V='0' F='Inh'/>
                                <Cell N='TextBkgndTrans' V='0' F='Inh'/>
                                <Cell N='QuickStyleLineColor' V='100'/>
                                <Cell N='QuickStyleFillColor' V='100'/>
                                <Cell N='QuickStyleShadowColor' V='100'/>
                                <Cell N='QuickStyleFontColor' V='100'/>
                                <Cell N='QuickStyleLineMatrix' V='1'/>
                                <Cell N='QuickStyleFillMatrix' V='1'/>
                                <Cell N='QuickStyleEffectsMatrix' V='1'/>
                                <Cell N='QuickStyleFontMatrix' V='1'/>
                                <Cell N='QuickStyleType' V='0'/>
                                <Cell N='QuickStyleVariation' V='0'/>
                                <Cell N='LineWeight' V='Themed' F='Inh'/>
                                <Cell N='LineColor' V='Themed' F='Inh'/>
                                <Cell N='LinePattern' V='Themed' F='Inh'/>
                                <Cell N='Rounding' V='Themed' F='Inh'/>
                                <Cell N='EndArrowSize' V='Themed' F='THEMEVAL()'/>
                                <Cell N='BeginArrow' V='Themed' F='THEMEVAL()'/>
                                <Cell N='EndArrow' V='Themed' F='THEMEVAL()'/>
                                <Cell N='LineCap' V='Themed' F='Inh'/>
                                <Cell N='BeginArrowSize' V='Themed' F='THEMEVAL()'/>
                                <Cell N='LineColorTrans' V='Themed' F='Inh'/>
                                <Cell N='CompoundType' V='Themed' F='Inh'/>
                                <Cell N='NoObjHandles' V='0' F='Inh'/>
                                <Cell N='NonPrinting' V='0' F='Inh'/>
                                <Cell N='NoCtlHandles' V='0' F='Inh'/>
                                <Cell N='NoAlignBox' V='0' F='Inh'/>
                                <Cell N='UpdateAlignBox' V='0' F='Inh'/>
                                <Cell N='HideText' V='0' F='Inh'/>
                                <Cell N='DynFeedback' V='0' F='Inh'/>
                                <Cell N='GlueType' V='0' F='Inh'/>
                                <Cell N='WalkPreference' V='0' F='Inh'/>
                                <Cell N='BegTrigger' V='0' F='No Formula'/>
                                <Cell N='EndTrigger' V='0' F='No Formula'/>
                                <Cell N='ObjType' V='0' F='Inh'/>
                                <Cell N='Comment' V='' F='Inh'/>
                                <Cell N='IsDropSource' V='0' F='Inh'/>
                                <Cell N='NoLiveDynamics' V='0' F='Inh'/>
                                <Cell N='LocalizeMerge' V='0' F='Inh'/>
                                <Cell N='NoProofing' V='0' F='Inh'/>
                                <Cell N='Calendar' V='0' F='Inh'/>
                                <Cell N='LangID' V='en-GB' F='Inh'/>
                                <Cell N='ShapeKeywords' V='' F='Inh'/>
                                <Cell N='DropOnPageScale' V='1' F='Inh'/>
                                <Section N='Character'>
                                    <Row IX='0'>
                                        <Cell N='Font' V='Themed' F='Inh'/>
                                        <Cell N='Color' V='Themed' F='Inh'/>
                                        <Cell N='Style' V='Themed' F='Inh'/>
                                        <Cell N='Case' V='0' F='Inh'/>
                                        <Cell N='Pos' V='0' F='Inh'/>
                                        <Cell N='FontScale' V='1' F='Inh'/>
                                        <Cell N='Size' V='0.1111111111111111'/>
                                        <Cell N='DblUnderline' V='0' F='Inh'/>
                                        <Cell N='Overline' V='0' F='Inh'/>
                                        <Cell N='Strikethru' V='0' F='Inh'/>
                                        <Cell N='DoubleStrikethrough' V='0' F='Inh'/>
                                        <Cell N='Letterspace' V='0' F='Inh'/>
                                        <Cell N='ColorTrans' V='0' F='Inh'/>
                                        <Cell N='AsianFont' V='Themed' F='Inh'/>
                                        <Cell N='ComplexScriptFont' V='Themed' F='Inh'/>
                                        <Cell N='ComplexScriptSize' V='-1' F='Inh'/>
                                        <Cell N='LangID' V='en-GB' F='Inh'/>
                                    </Row>
                                </Section>
                            </StyleSheet>
                        </StyleSheets>
                        <DocumentSheet NameU='TheDoc' IsCustomNameU='1' Name='TheDoc' IsCustomName='1' LineStyle='0' FillStyle='0' TextStyle='0'>
                            <Cell N='OutputFormat' V='0'/>
                            <Cell N='LockPreview' V='0'/>
                            <Cell N='AddMarkup' V='0'/>
                            <Cell N='ViewMarkup' V='0'/>
                            <Cell N='DocLockReplace' V='0' U='BOOL'/>
                            <Cell N='NoCoauth' V='0' U='BOOL'/>
                            <Cell N='DocLockDuplicatePage' V='0' U='BOOL'/>
                            <Cell N='PreviewQuality' V='0'/>
                            <Cell N='PreviewScope' V='0'/>
                            <Cell N='DocLangID' V='en-GB'/>
                            <Section N='User'>
                                <Row N='msvNoAutoConnect'>
                                    <Cell N='Value' V='1'/>
                                    <Cell N='Prompt' V='' F='No Formula'/>
                                </Row>
                            </Section>
                        </DocumentSheet>
                    </VisioDocument>"""

    def to_xml(self):
        return self.text
